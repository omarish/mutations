import asyncio
from collections import namedtuple, defaultdict
import inspect
import threading
import six

from . import fields
from . import error
from .util import wrap


Result = namedtuple('Result', ['success', 'return_value', 'errors'])
ValidationResult = namedtuple('ValidationResult', ['is_valid', 'errors'])


class RunThread(threading.Thread):
    def __init__(self, func):
        self.func = func
        self.result = None
        super().__init__()
        super().start()
        super().join()

    def run(self):
        self.result = asyncio.run(self.func())

class MutationBase(type):
    def __new__(mcs, name, bases, attrs):
        attrs.update({
            'fields': {},
            'validators': defaultdict(list),
            'extra_validators': defaultdict(list)
        })
        field_list, extra_validator_list = [], []

        for k, v in attrs.items():
            if isinstance(v, fields.FieldBase):
                field_list.append(k)
            elif isinstance(k, str) and k.startswith('validate_'):
                extra_validator_list.append(k)

        for f in field_list:
            field = attrs.pop(f)
            attrs['fields'][f] = field
            attrs['validators'][f].extend(wrap(field.validators))

        for v in extra_validator_list:
            validator = attrs.pop(v)
            attrs['extra_validators'][v].extend(wrap(validator))

        return super(MutationBase, mcs).__new__(mcs, name, bases, attrs)


@six.add_metaclass(MutationBase)
class Mutation(object):
    def __init__(self, name, inputs=None):
        self.name = name
        self.inputs = inputs or {}

    def __repr__(self):
        return '<Mutation {!r}>'.format(self.name)

    def __getattr__(self, name):
        if name in self.fields:
            return self._get_input(name)
        else:
            raise AttributeError

    def _validate(self):
        """Run all validations.

        We validate by doing the following:

        1. Validate base fields.
        2. Validate extra fields.

        If we encounter an error at any point along the way, mark that there has
        been at least one error. Then, try and continue validation, but if we
        run into another error (that is not a mutations error), terminate the
        validation process. This might be caused by whatever caused the initial
        validations.

        Returns a tuple: (was_successful, error_dict)
        """
        error_dict = error.ErrorDict()
        has_errors = False

        for field, validators in self.validators.items():
            value = self._get_input(field)
            for validator in validators:
                success, err = validator.validate(value)
                if not success:
                    error_dict[field].append(err)
                    has_errors = True

        for validator_name, funcs in self.extra_validators.items():
            for func in funcs:
                try:
                    func(self)
                except error.ValidationError as err:
                    has_errors = True
                    error_dict[validator_name].append(err.as_object())
                except Exception as exc:
                    if has_errors:
                        return (False, error_dict)
                    else:
                        has_errors = True
                        error_dict[validator_name].append(exc)

        return (not has_errors, error_dict)

    def _get_input(self, field):
        if field in self.inputs:
            return self.inputs[field]
        elif self.fields[field].has_default:
            return self.fields[field].default
        return

    def _execute_async(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            return RunThread(self.execute).result
        else:
            return asyncio.run(self.execute())

    def execute(self):
        raise error.ExecuteNotImplementedError(
            "`execute` should be implemented by the subclass.")

    @classmethod
    def run(cls, raise_on_error=False, **kwargs):
        """Validate the inputs and then calls execute() to run the command. """
        instance = cls(cls.__name__, inputs = kwargs)
        is_valid, error_dict = instance._validate()

        if not is_valid:
            if raise_on_error:
                raise error.MutationFailedValidationError(error_dict)
            else:
                return Result(success=False, return_value=None, errors=error_dict)

        if inspect.isawaitable(instance.execute()):
            result = instance._execute_async()
        else:
            result = instance.execute()
        return Result(success=True, return_value=result, errors=None)

    @classmethod
    def validate(cls, raise_on_error=False, **kwargs):
        instance = cls(cls.__name__, inputs = kwargs)
        is_valid, error_dict = instance._validate()
        if not is_valid:
            if raise_on_error:
                raise error.MutationFailedValidationError(error_dict)
            else:
                return ValidationResult(is_valid=False, errors=error_dict)
        return ValidationResult(is_valid=is_valid, errors=error_dict)
