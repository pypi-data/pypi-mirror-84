# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cornutils']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3,<4', 'numpy>=1,<2', 'scipy>=1,<2']

setup_kwargs = {
    'name': 'cornutils',
    'version': '0.2.2',
    'description': 'Utility functions',
    'long_description': "# cornutils\nPython package containing utility functions\n\n## Install\n```bash\npython3 -m pip install cornutils\n```\n\n## Example Usage of praktika\n```python\nimport numpy as np\nfrom cornutils.praktika import Data, PlotSettings, aio\n\nx = np.array([0,2,4,6,8,10,12,14,16,18,])\ny = np.array([2.8,5.2,6.8,9.6,11.2,14,15.6,17,19.8,21.4,])\ndelta_y = np.array([1.0,1.5,1.2,0.9,1.4,1.4,1.5,1.2,1.3,1.5,])\ndata = Data(x, y, sy=delta_y)\n\ns = PlotSettings(label_x='x-label', label_y = 'y-label',label_fit='Test')\n\ndef func(beta, x):\n    '''\n    Function to use for estimation, beta is an array with each parameter\n    '''\n    y = beta[0] + beta[1] * x\n    return y\n\naio(func, 2, data, s)\n```",
    'author': 'Cornelius Hoffmann',
    'author_email': 'coding@hoffmn.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cornelicorn/cornutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
