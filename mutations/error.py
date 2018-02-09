from collections import namedtuple
from six.moves import UserDict

class MutationError(Exception):
    pass


class ErrorDict(UserDict):
    def __init__(self, *args, **kwargs):
        self.default_factory = kwargs.pop('default_factory', list)
        UserDict.__init__(self, *args, **kwargs)

    def __getitem__(self, k):
        if not k in self.data:
            self.data[k] = self.default_factory()
        return self.data[k]

    def __add__(self, other):
        if self.default_factory != other.default_factory:
            raise MutationError("Cannot add two ErrorDicts with different default_factories.")
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


ErrorBody = namedtuple('ErrorBody', ['err', 'msg'])


class ValidationError(MutationError):
    def __init__(self, err=None, msg=None, *args, **kwargs):
        self.err = err
        self.msg = msg
        MutationError.__init__(self, *args, **kwargs)

    def __str__(self):
        return str(self.msg)

    def as_object(self):
        return ErrorBody(err=self.err, msg=self.msg)


class ExecuteNotImplementedError(NotImplementedError, MutationError):
    pass
