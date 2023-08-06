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
    'version': '1.2.1',
    'description': 'Keep those livestreams to watch whenever you want',
    'long_description': '[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# Streamkeeper\n\nWatches specified youtube channels and will automatically download any live streams the youtube channel posts, then converts to a video format. Optionally you can get notified over pushover.\n\n\n## Requirements\n\n`make setup`\n\nAlso requires [ffmpeg](https://ffmpeg.org/) and [streamlink](https://github.com/streamlink/streamlink), both need to be installed and executables in the current path.\n\n## Configuration\n\nFor now copy config.ini.sample to config.ini and fill in following the TODO comments.\n\n\n## Usage\n\n* `make build`\n* `make start` or `make daemon` to background it\n',
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
