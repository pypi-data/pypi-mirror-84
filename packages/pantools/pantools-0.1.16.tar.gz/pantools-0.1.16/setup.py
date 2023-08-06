# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pantools']

package_data = \
{'': ['*']}

install_requires = \
['imutil>=0.2.5,<0.3.0', 'numpy>=1.19.4,<2.0.0', 'opencv-python>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'pantools',
    'version': '0.1.16',
    'description': 'A collection of generic Python tools by Peter Andersson',
    'long_description': None,
    'author': 'Peter Andersson',
    'author_email': 'fshsweden@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
