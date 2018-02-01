import abc
from collections import namedtuple

import fields


MutationResult = namedtuple('MutationResult', ['result', 'value', 'errors'])

class MutationBase(type):
    def __new__(mcs, name, bases, attrs):
        attrs.update({
            'fields': {},
            'validators': {},
            'extra_validators': {}
        })
        field_list, extra_validator_list = [], []

        for k, v in attrs.items():
            if isinstance(v, fields.FieldBase):
                field_list.append(k)
            elif isinstance(k, str) and k.startswith('validate_'):
                extra_validator_list.append(k)

        for field in field_list:
            attrs['fields'][field] = attrs.pop(field)

        for field in extra_validator_list:
            attrs['extra_validators'][field] = attrs.pop(field)
        return super().__new__(mcs, name, bases, attrs)

    @abc.abstractmethod
    def run(cls, **kwargs):
        pass

class Mutation(metaclass=MutationBase):
    def validate(self):
        pass

    @classmethod
    def run(cls, **kwargs):
        pass




# class Mutation(type):
#     def __init__(self, name, inputs=None):
#         if not inputs:
#             inputs = {}
#         self.name = name
#         self.inputs = inputs
#         self.return_value = None
#         self.errors = None

#         self._fields = self._process_fields()

#     def __repr__(self):
#         return '<Mutation {!r}>'.format(self.name)

#     def _process_fields(self):
#         """Ensure all fields are valid definitions. """
#         # import ipdb; ipdb.set_trace()
#         pass

#     def validate(self):
#         pass

#     @classmethod
#     def execute(klass, *args, **kwargs):
#         raise NotImplementedError("This should be implemented in the subclass.")

#     @classmethod
#     def run(cls, **kwargs):
#         success, return_value = None, None
#         errors = ErrorDict()

#         # First, do base field validations and any custom validations.

#         # Assuming those pass, execute and capture the output.

#         try:
#             command = cls(cls.__name__, inputs=kwargs).execute()
#         except Exception as exc:
#             success = False
#         else:
#             success = True

#         return Result(success, return_value, errors)
