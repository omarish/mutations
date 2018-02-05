# TODO:

List of things we need to do/fix before releasing on PyPI:

### General

- [ ] Make sure you cannot create a field called "inputs"
- [ ] Make sure it raies if you give it a kwarg it doesn't know about.
- [ ] Think of a better way to pass exceptions. I don't like passing the
    `nameduple` in the Exception.

- [ ] Support for Python 2.X.
- [ ] Update README and provide more useful examples.
- [ ] Put test requirements into `test-requirements.txt`
- [ ] Make execute an `@abstractmethod`, so that an error gets raised if
    you don't define `execute` in your mutation subclass.
- [ ] Release on pypi.
- [ ] Support for running commands in an atomic (all or nothing) fashion,
    perhaps using a contextmanager.
- [x] Create setup.py file
- [x] Add `__version__`
- [x] Test that exceptions can be raised when you `run`.


### Testing

- [ ] Make sure default values get overridden if there's a user-provided value.
- [ ] Make sure command fails if you provide unexpected inputs.
- [ ] Make sure `Mutation.__getattr__` raises if you ask it for something that does not exist.


