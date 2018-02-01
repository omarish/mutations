class FieldBase(object):
    def __init__(self, name=None, **kwargs):
        self.name = name
        self.required = kwargs.pop('required', True)        

class ObjectField(FieldBase):
    pass

class BooleanField(FieldBase):
    pass

class CharField(FieldBase):
    pass
