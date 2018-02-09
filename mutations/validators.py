from .error import ErrorBody

class ValidatorBase(object):
    def validate(self, *args, **kwargs):
        valid = self.is_valid(*args, **kwargs)
        if not valid:
            return (False, self.get_error(*args, **kwargs))
        else:
            return (True, None)

    def is_valid(self):
        raise NotImplementedError()

    def get_error(self, val):
        err = self.__class__.__name__
        msg = "%s failed with input %r." % (self.__class__.__name__, val)
        return ErrorBody(err=err, msg=msg)
        

class RequiredValidator(ValidatorBase):
    def is_valid(self, val):
        return val is not None


class NotBlankValidator(ValidatorBase):
    def is_valid(self, val, strip=False):
        if strip:
            return val.strip() != ''
        else:
            return val != ''

class InstanceValidator(ValidatorBase):
    def __init__(self, instance_of, *args, **kwargs):
        self.instance_of = instance_of
        super(InstanceValidator, self).__init__(*args, **kwargs)

    def is_valid(self, val):
        return isinstance(val, self.instance_of)

class CustomValidator(ValidatorBase):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        super().__init__(self, *args, **kwargs)

    def is_valid(self, *args, **kwargs):
        return self.func(*args, **kwargs)

class YesValidator(ValidatorBase):
    def is_valid(self, *args, **kwargs):
        return True

class SavedObjectValidator(ValidatorBase):
    def is_valid(self, obj):
        return obj.pk is not None and obj.pk != ''
