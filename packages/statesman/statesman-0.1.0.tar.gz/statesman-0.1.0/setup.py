# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['statesman']
install_requires = \
['pydantic>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'statesman',
    'version': '0.1.0',
    'description': 'A modern state machine library.',
    'long_description': None,
    'author': 'Blake Watters',
    'author_email': 'blake@opsani.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
