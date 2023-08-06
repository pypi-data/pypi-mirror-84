# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_clubhouse', 'py_clubhouse.core', 'py_clubhouse.models']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'py-clubhouse',
    'version': '0.1.2',
    'description': 'Python client for Clubhouse',
    'long_description': '# py-clubhouse\n\n<p align="center">\n<a href="https://github.com/nickatnight/py-clubhouse"><img alt="Build Status" src="https://github.com/nickatnight/py-clubhouse/workflows/Run%20CI/badge.svg?branch=master"></a>\n<a href="https://codecov.io/gh/nickatnight/py-clubhouse">\n  <img src="https://codecov.io/gh/nickatnight/py-clubhouse/branch/master/graph/badge.svg?token=E03I4QK6D9"/>\n</a>\n<a href="https://pypi.org/project/py-clubhouse/"><img alt="Actions Status" src="https://img.shields.io/pypi/v/py-clubhouse?style=plastic"></a>\n</p>\n\n\nPython client for Clubhouse (started as a fork of [clubhouse-client](https://github.com/allardbrain/clubhouse-client))\n\n## Installation\n\nThe package is available on [pypi](https://pypi.org/project/py-clubhouse/) and can be installed like any other packages.\n\n    $ pip install py-clubhouse\n\n## Usage\n\nRefer to [Clubhouse API Docs](https://clubhouse.io/api/rest/v3/) for more information.\n\n```python\nfrom py_clubhouse import Clubhouse\n\nclubhouse = Clubhouse(\'your api key\')\n\nstory = clubhouse.get_story(1234)  # returns Story object\nworkflows = clubhouse.workflows()  # returns list of Workflow objects\nstories = clubhouse.search_stories("state:Staging")  # returns list of Story objects\n```\n\n## Development\n\n1. Clone repo\n2. Install [poetry](https://github.com/python-poetry/poetry/blob/master/README.md) globally.\n3. Activate virtual env `poetry shell`\n4. Install dependencies with `poetry install`\n5. Run pytest `poetry run pytest`\n\n## TODO\n\n* ~~add GHA workflow~~\n* ~~create models for relevant resources~~\n* moar tests\n* add c.r.u.d. methods for relevant models\n',
    'author': 'nickatnight',
    'author_email': 'nickkelly.858@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nickatnight/py-clubhouse/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
