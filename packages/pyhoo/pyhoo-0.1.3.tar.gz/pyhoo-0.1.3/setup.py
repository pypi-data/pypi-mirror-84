# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyhoo', 'pyhoo.models', 'pyhoo.parsers', 'pyhoo.types']

package_data = \
{'': ['*'], 'pyhoo': ['data/*']}

install_requires = \
['aiohttp>=3.6.1,<4.0.0', 'pandas>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'pyhoo',
    'version': '0.1.3',
    'description': 'Yet another unofficial Yahoo Finance API, but with concurrent requests',
    'long_description': '# Pyhoo\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Build Status](https://travis-ci.com/prouhard/pyhoo.svg?branch=master)](https://travis-ci.com/prouhard/pyhoo)\n[![codecov](https://codecov.io/gh/prouhard/pyhoo/branch/master/graph/badge.svg?token=6VJW1F01DL)](https://codecov.io/gh/prouhard/pyhoo)\n\n_Yet another unofficial Yahoo Finance API library but with concurrent requests._\n\n**Index**\n\n1. [Installation](#installation)\n1. [Usage](#usage)\n1. [Troubleshooting](#troubleshooting)\n1. [Contributing](#contributing)\n\n## Installation\n\n**Pyhoo requires Python >= 3.8**\n\n```bash\npip install pyhoo\n```\n\n## Usage\n\nPyhoo is **simple**:\n\n```python\nimport pyhoo\n\ntickers = [\'FB\', \'AAPL\', \'AMZN\', \'GOOGL\']\nstart = \'2020-02-01\'\nend = \'2020-11-02\'\n\nstock_prices = pyhoo.get(\'chart\', tickers, start=start, end=end, granularity="1d")\nfinancial_reports = pyhoo.get(\'fundamentals\', tickers, start=start, end=end)\noptions = pyhoo.get(\'options\', tickers, strikeMax=400.0)\n```\n\nThe result of `pyhoo.get` is a formatted `pandas.DataFrame` (here for stock prices):\n\n|     |  timestamp |   high |    low |   volume |   open |  close | adjclose | currency | symbol | exchangeName | instrumentType | regularMarketPrice | ... |\n| --: | ---------: | -----: | -----: | -------: | -----: | -----: | -------: | :------- | :----- | :----------- | :------------- | -----------------: | --: |\n|   0 | 1580481000 | 208.69 | 201.06 | 31359900 | 208.43 | 201.91 |   201.91 | USD      | FB     | NMS          | EQUITY         |             286.95 | ... |\n|   1 | 1580740200 | 205.14 |  202.5 | 15510500 | 203.44 | 204.19 |   204.19 | USD      | FB     | NMS          | EQUITY         |             286.95 | ... |\n|   2 | 1580826600 |  210.6 |  205.2 | 19628900 | 206.62 | 209.83 |   209.83 | USD      | FB     | NMS          | EQUITY         |             286.95 | ... |\n|   3 | 1580913000 | 212.73 | 208.71 | 12538200 | 212.51 | 210.11 |   210.11 | USD      | FB     | NMS          | EQUITY         |             286.95 | ... |\n|   4 | 1580999400 | 211.19 | 209.34 | 10567500 | 210.47 | 210.85 |   210.85 | USD      | FB     | NMS          | EQUITY         |             286.95 | ... |\n|   5 |        ... |    ... |    ... |      ... |    ... |    ... |      ... | ...      | ...    | ...          | ...            |                ... | ... |\n\nPyhoo is **fast**, it uses concurrency to fire multiple requests at the same time. You can request all the tickers of the S&P500 in one shot.\n\nPyhoo is **still in development**, feel free to add more endpoints thanks to the `Config` object !\n\nCurrently, it supports three endpoints:\n\n1. `chart`, for [OHLC](https://en.wikipedia.org/wiki/Open-high-low-close_chart) data, basically stock prices\n1. `fundamentals`, for financial data about the firm, see the [list of available reports](pyhoo/data/fundamentals_type_options.txt)\n1. `options`, for detailed information on each call and put at each strike on specific tickers\n\n## Troubleshooting\n\nIf running from a Jupyter Notebook, you may encounter the following error:\n\n```python\nRuntimeError: asyncio.run() cannot be called from a running event loop\n```\n\nThis is because Jupyter Notebooks are running themselves in an event loop, and it is a known issue with `asyncio.run`.\n\nThere is a workaround, a bit hacky but gets the job done, using [nest_asyncio](https://github.com/erdewit/nest_asyncio).\n\n```bash\npip install nest_asyncio\n```\n\nThen in the Notebook, before calling `pyhoo.get`:\n\n```python\nimport nest_asyncio\nnest_asyncio.apply()\n```\n\nAnd you should be ok !\n\n## Contributing\n\nContributions are welcome !\n\nPyhoo uses [poetry](https://python-poetry.org) as package manager. You can find the installation instructions [here](https://python-poetry.org/docs/#installation).\n\nIt is recommended to install the virtual environment in the project folder if you use VSCode, to help the linter resolve imports:\n\n```bash\npoetry config virtualenvs.path --unset\npoetry config virtualenvs.in-project true\n```\n\nOnce Poetry is configured, you can install required dependencies with:\n\n```bash\npoetry install\n```\n\nThe CI enforces strict typing, linting and coverage.\n',
    'author': 'ROUHARD Pierre',
    'author_email': 'pierrerouhard@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
