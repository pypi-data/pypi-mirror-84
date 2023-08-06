# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cnct',
 'cnct.client',
 'cnct.client.models',
 'cnct.help',
 'cnct.rql',
 'cnct.specs']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'connect-markdown-renderer>=1.0.0,<2.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'connect-api-client',
    'version': '21.0.0',
    'description': 'Connect Python OpenAPI Client',
    'long_description': None,
    'author': 'CloudBlue',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
