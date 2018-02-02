from collections import UserDict, namedtuple

class ErrorDict(UserDict):
    def __init__(self, *args, default_factory=list, **kwargs):
        self.default_factory = default_factory
        super().__init__(*args, **kwargs)

    def __getitem__(self, k):
        if not k in self.data:
            self.data[k] = self.default_factory()
        return self.data[k]

    def __add__(self, other):
        context = {}
        context.update(self)
        for key, val in other.items():
            if key in context:
                context[key] += val
            else:
                context[key] = val
        return ErrorDict(context, default_factory=self.default_factory)

    @property
    def is_empty(self):
        return not bool(self.data)


class MutationError(Exception):
    pass


ErrorBody = namedtuple('ErrorBody', ['err', 'msg'])

class ValidationError(MutationError):
    def __init__(self, err, msg=None, *args, **kwargs):
        self.err = err
        self.msg = msg
        super().__init__(*args, **kwargs)

    def __str__(self):
        return str(self.msg)

    def as_object(self):
        return ErrorBody(err=self.err, msg=self.msg or self.err)


class ExecuteNotImplementedError(NotImplementedError, MutationError):
    pass
