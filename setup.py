from distutils.core import setup

import mutations

setup(
    name='mutations',
    version=mutations.__version__,
    author='Omar Bohsali',
    author_email='me@omarish.com',
    packages=['mutations'],
    url="http://github.com/omarish/mutations",
    license='MIT',
    description='Encapsulate your business logic in command classes.',
    long_description="Mutations helps you split your complex business logic into command classes which are easier to test and maintain.",
    keywords=['business logic', 'django', 'fat models', 'thin models', 'input validation', 'commands', 'validation'],
    install_requires=[],
)
