# Mutations

Encapsulate your business logic into commands.

## Example

```python
import mutations

class EmailToBouncedMessage(mutations.Mutation):
    email = mutations.fields.Object(required=True)
    send_welcome_email = mutation.fields.Boolean(required=False, default=False)

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

        This will raise `mutation.RuntimeError` if an error was encountered
        during execution.
        """
        new_object = "this is the new object"
        # Do the heavy lifting here. 
        # You might want to wrap this in a django atomic block.
        if self.send_welcome_email:
            # You can access the inputs here.
            pass
        return new_object
```

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