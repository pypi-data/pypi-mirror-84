# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamkeeper', 'streamkeeper.services']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=1.12.5,<2.0.0',
 'python-daemon>=2.2.4,<3.0.0',
 'python-pushover>=0.4,<0.5',
 'streamlink>=1.7.0,<2.0.0',
 'youtube-python>=1.0.13,<2.0.0']

entry_points = \
{'console_scripts': ['streamkeeper = streamkeeper.streamkeeper:main']}

setup_kwargs = {
    'name': 'streamkeeper',
    'version': '1.1',
    'description': 'Keep those livestreams to watch whenever you want',
    'long_description': None,
    'author': 'Shane Dowling',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
