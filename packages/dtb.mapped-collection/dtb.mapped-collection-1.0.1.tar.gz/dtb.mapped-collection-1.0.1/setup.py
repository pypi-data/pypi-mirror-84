# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mapped_collection']
setup_kwargs = {
    'name': 'dtb.mapped-collection',
    'version': '1.0.1',
    'description': '',
    'long_description': None,
    'author': 'Dima Doroshev',
    'author_email': 'dima@doroshev.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
