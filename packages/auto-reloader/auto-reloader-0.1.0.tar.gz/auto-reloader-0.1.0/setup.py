# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['auto_reloader']
setup_kwargs = {
    'name': 'auto-reloader',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'moisutsu',
    'author_email': 'moisutsu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/moisutsu/auto-reloader',
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
