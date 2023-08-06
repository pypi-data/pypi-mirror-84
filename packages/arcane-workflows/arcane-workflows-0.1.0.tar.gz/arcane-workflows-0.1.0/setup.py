# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-workflows==0.1.0']

setup_kwargs = {
    'name': 'arcane-workflows',
    'version': '0.1.0',
    'description': 'Package description',
    'long_description': '# Arcane workflows\n\nOverride the [Workflows API client](https://googleapis.dev/python/workflows/latest/index.html)\n',
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
