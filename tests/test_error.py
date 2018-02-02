from mutations.error import ErrorDict


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
