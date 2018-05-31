# Mutations

[![pypi-version]][pypi]

Compose your business logic into commands that sanitize and validate input.

## Install

```bash
$ pip install mutations
```

## How it Works:

1. Subclass `mutations.Mutation`
2. Define your inputs.
3. Define an `execute` method in your command.
4. Run it, like this: `SimpleMutation.run(foo='bar')`

To learn more, see [this blog post](https://omarish.com/2018/02/17/mutations.html).

## Example

```python
import mutations

class UserSignup(mutations.Mutation):
    """Define the inputs to your mutation here. """
    email = mutations.fields.CharField(required=True)
    full_name = mutations.fields.CharField(required=True)
    send_welcome_email = mutations.fields.Boolean(required=False, default=True)

    def validate_email_address(self):
        """Custom validation for a field.

        If you encounter any validation errors and want to raise, you should
        raise mutation.ValidationError or some sublcass thereof. Otherwise, it
        assumes there were no problems.

        Any function beginning with `validate_` is assumed to be a validator
        function and will be run before the mutation can execute.
        """
        if not self.email.is_valid():
            raise mutations.ValidationError("email_not_valid", "Email is not valid.")

    def execute(self):
        """Executes the mutation.

        This method does the heavy lifting. You can call it by calling .run() on
        your mutation class.
        """
        user = User.objects.create(email=self.email, name=self.full_name)
        if self.send_welcome_email:
            EmailServer.deliver(recipient = self.email)
        return user
```

## Calling Commands

```python
>>> result = UserSignup.run(email=email, full_name="Bob Boblob")
>>> result.success
True
>>> result.return_value
<User id=...>
>>> result.errors

result = ...

```

```python
>>> result = UserSignup.run(email=None)
>>> result.success
False
>>> result.errors
mutations.ErrorDict({
  'email': ['email_not_valid']
})
>>> result.value
None
```

## Testing

```bash
$ make tests
```

# Versioning

This project uses [Semantic Versioning][semver].

# Thanks

Thanks to Cypriss for the excellent Ruby [Mutations Gem][1]. I created this library because I was looking for something similar for Python.

[1]: https://github.com/cypriss/mutations
[semver]: https://semver.org/
[pypi-version]: https://img.shields.io/pypi/v/mutations.svg
[pypi]: https://pypi.org/project/mutations/
