from collections import namedtuple, defaultdict
import six

from . import fields
from . import error
from .util import wrap

Result = namedtuple('Result', ['success', 'return_value', 'errors'])


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

    def _do_validation(self):
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

    def execute(self):
        raise error.ExecuteNotImplementedError(
            "`execute` should be implemented by the subclass.")

    @classmethod
    def run(cls, raise_on_error=False, **kwargs):
        """Validate the inputs and then calls execute() to run the command. """
        instance = cls(cls.__name__, inputs = kwargs)
        is_valid, error_dict = instance._do_validation()

        if not is_valid:
            if raise_on_error:
                raise error.ValidationError('invalid_inputs')
            else:
                return Result(success=False, return_value=None, errors=error_dict)

        result = instance.execute()
        return Result(success=True, return_value=result, errors=None)
