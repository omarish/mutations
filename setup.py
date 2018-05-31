import re
from distutils.core import setup
from os import path

meta_file = open("mutations/metadata.py").read()
md = dict(re.findall(r"__([a-z]+)__\s*=\s*'([^']+)'", meta_file))

project_path = path.abspath(path.dirname(__file__))

with open(path.join(project_path, 'README.md')) as f:
    long_description = f.read()

setup(
    name='mutations',
    version=md['version'],
    author=md['author'],
    author_email=md['authoremail'],
    packages=['mutations'],
    url="http://github.com/omarish/mutations",
    license='MIT',
    description='Encapsulate your business logic in command classes.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['business logic', 'django', 'fat models', 'thin models', 'input validation', 'commands', 'validation'],
    install_requires=['six>=1.11.0'],
)
