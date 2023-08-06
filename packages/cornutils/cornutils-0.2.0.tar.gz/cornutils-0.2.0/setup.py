# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cornutils']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.2,<4.0.0', 'numpy>=1.19.4,<2.0.0', 'scipy>=1.5.4,<2.0.0']

setup_kwargs = {
    'name': 'cornutils',
    'version': '0.2.0',
    'description': 'Utility functions',
    'long_description': '# cornutils\nPython package containing utility functions\n',
    'author': 'Cornelius Hoffmann',
    'author_email': 'coding@hoffmn.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cornelicorn/cornutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
