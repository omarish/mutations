from mutations import fields, Mutation
from mutations.error import ValidationError

existing_users = [
    'user@example.com',
    'user2@example.com'
]

class UserSignup(Mutation):
    email = fields.CharField()
    name = fields.CharField()

    def validate_no_existing_user(self):
        """Ensure no user already exists with this email. """
        if self.email in existing_users:
            raise ValidationError("email_exists")
    
    def validate_email(self):
        if "aol.com" in self.email:
            raise ValidationError("invalid_email")
    
    def validate_name(self):
        parts = self.name.split()
        if len(parts) < 2:
            raise ValidationError("need_full_name", "Please enter a full name.")
        
class TestComplex(object):
    def test_validations(self):
        data = { 'email': 'user@example.com', 'name': 'Bob' }
        result = UserSignup.run(**data)
        assert not result.success
        err_keys = result.errors.keys()
        assert 'validate_no_existing_user' in err_keys
        assert 'validate_name' in err_keys

    def test_missing_field(self):
        data = { 'email': 'user@example.com' }
        result = UserSignup.run(**data)
        assert not result.success
        err_keys = result.errors.keys()
        assert 'name' in err_keys