# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['udotu']
setup_kwargs = {
    'name': 'udotu',
    'version': '0.0.1',
    'description': 'print debugging for a more civilized age',
    'long_description': None,
    'author': 'Jon Skulski',
    'author_email': 'jskulski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
