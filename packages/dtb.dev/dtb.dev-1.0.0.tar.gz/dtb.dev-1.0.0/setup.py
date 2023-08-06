# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dtb_dev']
extras_require = \
{'devtools': ['isort>=5.6.1,<6.0.0',
              'ptipython>=1.0.1,<2.0.0',
              'pre-commit>=2.7.1,<3.0.0',
              'autoflake>=1.4,<2.0']}

setup_kwargs = {
    'name': 'dtb.dev',
    'version': '1.0.0',
    'description': 'DTB: Base dev tools',
    'long_description': None,
    'author': 'Dima Doroshev',
    'author_email': 'dima@doroshev.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
