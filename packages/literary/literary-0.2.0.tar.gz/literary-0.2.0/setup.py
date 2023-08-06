# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['literary']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'astunparse>=1.6.3,<2.0.0',
 'nbconvert>=6.0.7,<7.0.0',
 'nbformat[fast]>=5.0.8,<6.0.0',
 'traitlets>=5.0.5,<6.0.0']

entry_points = \
{'console_scripts': ['literary-build = literary.build:run']}

setup_kwargs = {
    'name': 'literary',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Angus Hollands',
    'author_email': 'goosey15@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
