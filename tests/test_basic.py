import pytest

import mutations
from mutations.validators import RequiredValidator, InstanceValidator, NotBlankValidator
from mutations import error, fields, validators


_yes = "this worked!"
_email = "user@example.com"
_name = "Bob Boblob"
_band = 'Nickelback'

class SimpleMutation(mutations.Mutation):
    email = fields.CharField(required=True)
    send_welcome_email = fields.BooleanField(required=False, default=False)

    def execute(self):
        return "".join([_yes, _email])

class TestBasics(object):
    def test_basics(self):
        result = SimpleMutation.run(name=_name, email=_email)
        assert result is not None
        assert result.success
        assert result.errors is None
        assert result.return_value == "".join([_yes, _email])

    def test_field_validators(self):
        assert RequiredValidator in map(type, SimpleMutation.fields['email'].validators)

    def test_requires_execute(self):
        """Make sure there's an error if you define a mutation without an 
        execute() method. """
        with pytest.raises(error.ExecuteNotImplementedError):
            class MutationWithoutExecute(mutations.Mutation):
                pass
            MutationWithoutExecute.run(email = _email)

class SimpleMutationWithDefault(mutations.Mutation):
    email = fields.CharField(required=True)
    favorite_band = fields.CharField(required=False, default=_band)

    def execute(self):
        return self.favorite_band

class TestDefaults(object):
    def test_default_values(self):
        result = SimpleMutationWithDefault.run(email=_email)
        assert result.success
        assert result.return_value == _band

class TestValidators():
    def test_basic_validators(self):
        result = SimpleMutation.run(email = None)
        assert result.success is False
        assert 'email' in result.errors

    def test_required_validator(self):
        _ = RequiredValidator().is_valid
        assert not _(None)
        assert _(True)
        assert _("foo")

    def test_not_blank_validator(self):
        _ = NotBlankValidator().is_valid
        assert not _('')
        assert _('foo')

    def test_instance_validator(self):
        _ = InstanceValidator(list).is_valid
        assert not _("foo")
        assert _([1, 1, 2, 3, 5, 8, 13, 21])
        assert not _((1, 1, 1))
