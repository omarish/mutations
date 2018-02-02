from . import validators

class FieldBase(object):
    def __init__(self, name=None, **kwargs):
        self.name = name
        self.required = kwargs.pop('required', True)
        self.blank = kwargs.pop('blank', False)

        self.has_default = 'default' in kwargs
        self.default = kwargs.pop('default', None)

    @property
    def validators(self):
        _ = []
        if self.required:
            _.append(validators.RequiredValidator())
        if self.blank == False:
            _.append(validators.NotBlankValidator())
        return _

class ObjectField(FieldBase):
    pass

class BooleanField(FieldBase):
    @property
    def validators(self):
        return validators.InstanceValidator(instance_of=bool)
        

class CharField(FieldBase):
    @property
    def validators(self):
        return validators.InstanceValidator(instance_of=str)

class DuckField(FieldBase):
    """Use this for duck-typing. """
    def __init__(self, instance_of, *args, **kwargs):
        self.instance_of = instance_of
        super().__init__(*args, **kwargs)

    @property
    def validators(self):
        return validators.InstanceValidator(instance_of=self.instance_of)