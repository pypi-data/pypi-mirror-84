# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['met_api']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.6.1,<2.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'met-api',
    'version': '0.1.0',
    'description': '"Metropolitain Museum of Art API client."',
    'long_description': None,
    'author': 'Yevhenii Zotkin',
    'author_email': 'yevhenii.zotkin@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
