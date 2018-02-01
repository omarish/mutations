import pytest

import mutations


class SimpleMutation(mutations.Mutation):
    email = mutations.fields.CharField(required=True)
    send_welcome_email = mutations.fields.BooleanField(required=False, default=False)

    def validate_email_address(self):
        pass

    def execute(self):
        print("execute")


class SimpleMutation(mutations.Mutation):
    name = mutations.fields.CharField()
    email = mutations.fields.CharField()
    location = mutations.fields.CharField(required = False)

def test_basic_setup():
    result = SimpleMutation.run(name="Omar Bohsali", email="me@omarish.com")
    assert result is not None
    assert result.success

def test_extra_validators():
    # Make sure extra validators pass through
    pass

"""
Things to Test:

1. It raises an error if you don't define run in your own mutation.

"""