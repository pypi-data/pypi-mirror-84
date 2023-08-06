# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sched2']
setup_kwargs = {
    'name': 'sched2',
    'version': '0.1.0',
    'description': 'Event scheduler',
    'long_description': None,
    'author': 'Pedro Rodrigues',
    'author_email': 'medecau@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/medecau/sched2',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
