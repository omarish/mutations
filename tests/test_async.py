import mutations
import pytest
import asyncio

_str = "My email is"
_email = "foo@bar.com"


class SimpleAsyncMutation(mutations.Mutation):
    email = mutations.fields.CharField(required=True)

    async def execute(self):
        await asyncio.sleep(1)
        return f"{_str} {self.email}"


class TestSimpleAsync():
    @pytest.mark.asyncio
    async def test_await_works(self):
        result = SimpleAsyncMutation.run(email=_email)
        assert result.success
        assert result.return_value == f"{_str} {_email}"

    @pytest.mark.asyncio
    async def test_validation_works(self):
        result = SimpleAsyncMutation.run(email=None)
        assert result.success is False
        assert 'email' in result.errors

    @pytest.mark.asyncio
    async def test_raise_error_succeeds(self):
        with pytest.raises(mutations.error.ValidationError):
            result = SimpleAsyncMutation.run(raise_on_error=True)

    def test_validation_only(self):
        v = SimpleAsyncMutation.validate(raise_on_error=False)
        assert isinstance(v, mutations.core.ValidationResult)

        with pytest.raises(mutations.error.MutationFailedValidationError):
            v = SimpleAsyncMutation.validate(raise_on_error=True)

        v = SimpleAsyncMutation.validate(email="user@example.com")
        assert isinstance(v, mutations.core.ValidationResult)
        assert v.is_valid == True
