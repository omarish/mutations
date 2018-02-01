class ValidatorBase(object):
    pass


class RequiredValidator(ValidatorBase):
    @classmethod
    def is_valid(cls, val):
        return val is not None


class NotBlankValidator(ValidatorBase):
    @classmethod
    def is_valid(cls, val):
        return val != ''
