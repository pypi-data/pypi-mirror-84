# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keep2roam']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'marshmallow>=3.9.0,<4.0.0']

entry_points = \
{'console_scripts': ['k2r = keep2roam:k2r']}

setup_kwargs = {
    'name': 'keep2roam',
    'version': '1.1',
    'description': 'Convert Google Keep Takeout Files to Roam Daily Notes Pages',
    'long_description': '# Google Keep to Roam Daily Notes\n\n![build](https://github.com/adithyabsk/keep2roam/workflows/build/badge.svg?branch=master)\n[![codecov](https://codecov.io/gh/adithyabsk/keep2roam/branch/master/graph/badge.svg?token=RPI1KJKN8G)](https://codecov.io/gh/adithyabsk/keep2roam)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/keep2roam?style=plastic)\n![PyPI - Downloads](https://img.shields.io/pypi/dw/keep2roam?style=plastic)\n![GitHub](https://img.shields.io/github/license/adithyabsk/keep2roam?logo=6cc644&style=plastic)\n![Black](https://img.shields.io/badge/code%20style-black-000000.svg)\n![Twitter Follow](https://img.shields.io/twitter/follow/adithya_balaji?style=social)\n\nConvert a Takeout of Google Keep to Roam Daily Notes for the day that each\nsnippet was written. If multiple notes were written on the same day, they are\nmerged together.\n\n## Installation\n\nFirst, go to [Google Takeout](https://takeout.google.com/settings/takeout) and\nrequest a dump of your Google Keep data. Then unzip the folder that Google sends\nyou.\n\nThe following steps work well on Unix systems but on Windows it would be quite\nsimilar.\n\n```console\n$ cd ~/Downloads\n$ tar -xvf takeout-{ID}.zip\n$ pip install keep2roam\n$ mkdir markdown\n$ k2r -h\nUsage: k2r [OPTIONS] SRC DEST\n\n  Convert SRC Google Keep Takeout dump and write to DEST folder.\n\n  Assumes SRC exists and creates DEST folder if it does not exist.\n\nOptions:\n  --version   Prints the CLI version\n  -h, --help  Show this message and exit.\n$ k2r Takeout/Keep markdown\nFound X Google Keep json files...\n```\n\n## Upload Limit\n\nNow take these files and upload them to Roam. To upload more than 10 files at a\ntime, use [this workaround.](https://forum.roamresearch.com/t/workaround-for-10-file-limit-on-markdown-import/558/2)\n',
    'author': 'Adithya Balaji',
    'author_email': 'adithyabsk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adithyabsk/keep2roam',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
