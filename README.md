# Mutations

Compose your business logic into commands that sanitize and validate input.

## How it Works:

1. Subclass `mutations.Mutation`
2. Define your inputs.
3. Define an `execute` method in your command.
4. Run it, lke this: `SimpleMutation.run(foo='bar')`

## Pre-Alpha

This is still in pre-alpha. See TODO for a list of things that we need to get
done before officially releasing on PyPI.

## Example

```python
import mutations

class EmailToBouncedMessage(mutations.Mutation):
    email = mutations.fields.CharField(required=True)
    send_welcome_email = mutations.fields.Boolean(required=False, default=False)

    def validate_email_object(self):
        """Custom validation for a field.

        If you encounter any validation errors and want to raise, you should
        raise mutation.ValidationError or some sublcass thereof. Otherwise, it
        assumes there were no problems.

        Any function beginning with `validate_` is assumed to be a validator function.
        """
        if not self.email.is_valid():
            raise mutations.ValidationError("email_not_valid", "Email is not valid.")

    def execute(self):
        """Executes the mutation.

        This method does the heavy lifting. You can call it by calling .run() on
        your mutation class.
        """
        new_object = "this is the new object"
        if self.send_welcome_email:
            # You can access the inputs here, like this.
            PersonalEmailServer.deliver(recipient = self.email)

        return new_object
```

## Calling Commands

```python
>>> result = EmailToBouncedMessage.run(email=email, send_welcome_email=True)
>>> result.success
True
>>> result.value
"this is the new object"
>>> result.errors
```

```python
>>> result = EmailToBouncedMessage.run(email = None)
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

Thanks to Cypriss for the excellent Ruby [Mutations Gem][1]. I created this
library because I was looking for something similar for Python.

[1]: https://github.com/cypriss/mutations
[semver]: https://semver.org/
