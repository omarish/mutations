from collections import UserDict

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


class ValidationError(MutationError):
    pass


class ExecuteNotImplementedError(NotImplementedError, MutationError):
    pass
