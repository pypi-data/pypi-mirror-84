# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asahi']

package_data = \
{'': ['*']}

extras_require = \
{'extras': ['asahi-extras>=0.1.0,<0.2.0']}

setup_kwargs = {
    'name': 'asahi',
    'version': '0.1.1',
    'description': 'A small package to provide utility functions to libraries that has optional installs / extras',
    'long_description': '# `asahi`\n\n![Python package](https://github.com/kalaspuff/asahi/workflows/Python%20package/badge.svg)\n[![pypi](https://badge.fury.io/py/asahi.svg)](https://pypi.python.org/pypi/asahi/)\n[![Made with Python](https://img.shields.io/pypi/pyversions/asahi)](https://www.python.org/)\n[![Type hinted - mypy validated](https://img.shields.io/badge/typehinted-yes-teal)](https://github.com/kalaspuff/asahi)\n[![MIT License](https://img.shields.io/github/license/kalaspuff/asahi.svg)](https://github.com/kalaspuff/asahi/blob/master/LICENSE)\n[![Code coverage](https://codecov.io/gh/kalaspuff/asahi/branch/master/graph/badge.svg)](https://codecov.io/gh/kalaspuff/asahi/tree/master/asahi)\n\n*A small package to provide utility functions to libraries that has optional installs (so called "extras").*\n\n\n## Installation with `pip`\nLike you would install any other Python package, use `pip`, `poetry`, `pipenv` or your weapon of choice.\n```\n$ pip install asahi\n```\n\n\n## Usage and examples\n\n#### Use-case\n```\nimport asahi\n\n```\n',
    'author': 'Carl Oscar Aaro',
    'author_email': 'hello@carloscar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kalaspuff/asahi',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
