import pytest
import unittest
import mutations
import math


class FooClass(object):
    def a(self):
        return "a"


class CommandForTest(mutations.Mutation):
    batch_size = mutations.fields.ObjectField(instance_of=int, required=True, blank=False)
    input_object = mutations.fields.ObjectField(instance_of=FooClass, required=True, blank=True)

    def validate_is_square(self):
        root = self.batch_size ** (1 / 2)
        if not root == int(root):
            raise mutations.ValidationError("not_a_square")

    def validate_input_object(self):
        if not self.input_object.a() == "b":
            raise mutations.ValidationError("incorrect_response")


def test_resillience():
    instance = FooClass()
    result = CommandForTest.run(batch_size=None, input_object=instance)
    assert not result.success


def test_missing_object():
    def validate_nested_method(self):
        if not self.input_object.b.c() == "d":
            raise mutations.ValidationError('invalid_object')
    CommandForTest.validate_nested_method = validate_nested_method

    def validate_triple_nested_method(self):
        if not self.input_object.b.c.d() == "e":
            raise mutations.ValidationError('invalid_object')
    CommandForTest.validate_triple_nested_method = validate_triple_nested_method

    result = CommandForTest.run(input_object=None)
    assert not result.success
