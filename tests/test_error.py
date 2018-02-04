import pytest

from mutations.error import ErrorDict
import mutations
from mutations import fields

class TestErrorDict(object):
    def test_basics_dict(self):
        e = ErrorDict()
        assert e.is_empty
        e['foo'].append('bar')
        assert dict(e) == {'foo': ['bar']}
        assert not e.is_empty

    def test_addition_simple(self):
        a = ErrorDict({'a': ['b']})
        b = ErrorDict({'c': ['d']})
        c = a + b
        assert dict(c) == {'a': ['b'], 'c': ['d']}

    def test_addition_deep(self):
        a = ErrorDict({'a': ['b']})
        b = ErrorDict({'a': ['c', 'd'], 'c': ['e']})
        c = a + b
        assert c['a'] == ['b', 'c', 'd']
        assert c['c'] == ['e']
        assert isinstance(c, ErrorDict)


class ErrantMutation(mutations.Mutation):
    email = fields.CharField(required=True)

    def execute(self):
        temp = self.this_field_does_not_exist
        return "123"

class TestErrorHandling(object):
    def test_raise_on_invalid_attribute(self):
        with pytest.raises(AttributeError):
            ErrantMutation.run(email="user@example.com")
