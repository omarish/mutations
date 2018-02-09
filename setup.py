from distutils.core import setup

import mutations

setup(
    name='Mutations',
    version=mutations.__version__,
    author='Omar Bohsali',
    author_email='me@omarish.com',
    packages=['mutations'],
    url="http://github.com/omarish/mutations",
    license='LICENSE',
    description='Encapsulate your business logic.',
    long_description="Mutations helps you split your complex business logic into command classes which are easier to test and maintain.",
    install_requires=[],
)
