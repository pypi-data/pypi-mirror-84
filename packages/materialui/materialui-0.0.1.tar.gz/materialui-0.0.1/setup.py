# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['materialui']
setup_kwargs = {
    'name': 'materialui',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Vladislav Ishchuk',
    'author_email': 'vlad.ischuck2006@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
