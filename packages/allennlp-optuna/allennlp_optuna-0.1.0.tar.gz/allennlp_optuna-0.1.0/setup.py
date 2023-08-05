# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['allennlp_optuna', 'allennlp_optuna.commands']

package_data = \
{'': ['*']}

install_requires = \
['allennlp>=1.0.0', 'optuna>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'allennlp-optuna',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'himkt',
    'author_email': 'himkt@cookpad.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
