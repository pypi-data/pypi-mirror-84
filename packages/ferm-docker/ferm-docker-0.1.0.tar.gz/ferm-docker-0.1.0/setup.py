# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ferm_docker']

package_data = \
{'': ['*'], 'ferm_docker': ['templates/*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0', 'docker>=4.3.1,<5.0.0']

entry_points = \
{'console_scripts': ['ferm-docker = ferm_docker:main']}

setup_kwargs = {
    'name': 'ferm-docker',
    'version': '0.1.0',
    'description': 'Automatically generate ferm firewall configurations for a local docker instance',
    'long_description': None,
    'author': 'Martin Weinelt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
