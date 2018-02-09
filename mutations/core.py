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
        errors = self._validate_base_fields() + self._validate_extra_fields()
        if errors.is_empty:
            return (True, None)
        else:
            return (False, errors)

    def _validate_base_fields(self):
        _ = error.ErrorDict()
        for field, validators in self.validators.items():
            value = self._get_input(field)
            for validator in validators:
                success, err = validator.validate(value)
                if not success:
                    _[field].append(err)
        return _

    def _validate_extra_fields(self):
        _ = error.ErrorDict()
        for name, funcs in self.extra_validators.items():
            for func in funcs:
                try:
                    func(self)
                except error.ValidationError as err:
                    _[name].append(err.as_object())
        return _

    def _get_input(self, field):
        if field in self.inputs:
            return self.inputs[field]
        elif self.fields[field].has_default:
            return self.fields[field].default

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
