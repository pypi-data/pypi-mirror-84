# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keep2roam']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'marshmallow>=3.9.0,<4.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=2.0.0,<3.0.0']}

entry_points = \
{'console_scripts': ['k2r = keep2roam:k2r']}

setup_kwargs = {
    'name': 'keep2roam',
    'version': '1.0',
    'description': 'Convert Google Keep Takeout Files to Roam Daily Notes Pages',
    'long_description': '# Google Keep to Roam Daily Notes\n\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/adithyabsk/keep2roam/build?color=6cc644&logo=github&style=plastic)\n![Codecov](https://img.shields.io/codecov/c/github/adithyabsk/keep2roam?color=6cc644&style=plastic)\n![GitHub](https://img.shields.io/github/license/adithyabsk/keep2roam?logo=6cc644&style=plastic)\n![Black](https://img.shields.io/badge/code%20style-black-000000.svg)\n![Twitter Follow](https://img.shields.io/twitter/follow/adithya_balaji?style=social)\n\nConvert a Takeout of Google Keep to Roam Daily Notes for the day that each\nsnippet was written. If multiple notes were written on the same day, they are\nmerged together.\n\n## Installation\n\nFirst, go to [Google Takeout](https://takeout.google.com/settings/takeout) and\nrequest a dump of your Google Keep data. Then unzip the folder that Google sends\nyou.\n\nThe following steps work well on Unix systems but on Windows it would be quite\nsimilar.\n\n```console\n$ cd ~/Downloads\n$ tar -xvf takeout-{ID}.zip\n$ pip install git+https://github.com/adithyabsk/keep2roam.git\n$ mkdir markdown\n$ k2r -h\nUsage: k2r [OPTIONS] SRC DEST\n\n  Convert SRC Google Keep Takeout dump and write to DEST folder.\n\n  Assumes SRC exists and creates DEST folder if it does not exist.\n\nOptions:\n  --version   Prints the CLI version\n  -h, --help  Show this message and exit.\n$ k2r Takeout/Keep markdown\nFound X Google Keep json files...\n```\n\n## Upload Limit\n\nNow take these files and upload them to Roam. To upload more than 10 files at a\ntime, use [this workaround.](https://forum.roamresearch.com/t/workaround-for-10-file-limit-on-markdown-import/558/2)\n',
    'author': 'Adithya Balaji',
    'author_email': 'adithyabsk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adithyabsk/keep2roam',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
