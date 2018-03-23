import re
from distutils.core import setup

meta_file = open("mutations/metadata.py").read()
md = dict(re.findall(r"__([a-z]+)__\s*=\s*'([^']+)'", meta_file))

setup(
    name='mutations',
    version=md['version'],
    author=md['author'],
    author_email=md['authoremail'],
    packages=['mutations'],
    url="http://github.com/omarish/mutations",
    license='MIT',
    description='Encapsulate your business logic in command classes.',
    long_description="Mutations helps you split your complex business logic into command classes which are easier to test and maintain.",
    keywords=['business logic', 'django', 'fat models', 'thin models', 'input validation', 'commands', 'validation'],
    install_requires=['six>=1.11.0'],
)
