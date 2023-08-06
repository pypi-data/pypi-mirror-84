# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pkp']
install_requires = \
['colorama>=0.4.4,<0.5.0', 'pykeepass>=3.2.1,<4.0.0']

setup_kwargs = {
    'name': 'pkp',
    'version': '0.6.1',
    'description': 'Straightforward CLI for KeePass - powered by pykeepass',
    'long_description': None,
    'author': 'Philipp Schmitt',
    'author_email': 'philipp@schmitt.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
