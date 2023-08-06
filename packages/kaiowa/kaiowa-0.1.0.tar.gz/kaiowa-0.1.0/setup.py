# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kaiowa', 'kaiowa.backends', 'kaiowa.core', 'kaiowa.migrations', 'kaiowa.orm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kaiowa',
    'version': '0.1.0',
    'description': 'Asynchronous Database ORM for Python.',
    'long_description': None,
    'author': 'Eduardo Rezende',
    'author_email': 'eduardorbr7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
