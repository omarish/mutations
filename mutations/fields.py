from . import validators

class FieldBase(object):
    def __init__(self, name=None, **kwargs):
        self.name = name
        self._add_validators(**kwargs)

    def _add_validators(self, **kwargs):
        self.required = kwargs.pop('required', True)
        self.blank = kwargs.pop('blank', False)
        self.saved = kwargs.pop('saved', False)
        self.has_default = 'default' in kwargs
        self.default = kwargs.pop('default', None)
        self.saved = kwargs.pop('saved', False)
        self.instance_of = kwargs.pop('instance_of', None)

    @property
    def validators(self):
        _ = []
        if self.required:
            _.append(validators.RequiredValidator())
        if self.blank == False:
            _.append(validators.NotBlankValidator())
        if self.saved:
            _.append(validators.SavedObjectValidator())
        if self.instance_of:
            _.append(validators.InstanceValidator(self.instance_of))
        return _


class ObjectField(FieldBase):
    @property
    def validators(self):
        return validators.YesValidator()

class BooleanField(FieldBase):
    @property
    def validators(self):
        return validators.InstanceValidator(instance_of=bool)

class CharField(FieldBase):
    @property
    def validators(self):
        return validators.InstanceValidator(instance_of=str)

class DictField(FieldBase):
    @property
    def validators(self):
        return validators.InstanceValidator(instance_of=dict)

class DuckField(FieldBase):
    """Use this for duck-typing. """
    def __init__(self, instance_of, *args, **kwargs):
        self.instance_of = instance_of
        super().__init__(*args, **kwargs)

    @property
    def validators(self):
        return validators.InstanceValidator(instance_of=self.instance_of)
