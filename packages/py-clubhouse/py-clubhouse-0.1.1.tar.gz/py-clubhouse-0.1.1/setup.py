# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_clubhouse', 'py_clubhouse.models', 'py_clubhouse.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'py-clubhouse',
    'version': '0.1.1',
    'description': 'Python client for Clubhouse',
    'long_description': '# py-clubhouse\n\n<p align="center">\n<a href="https://codecov.io/gh/nickatnight/py-clubhouse">\n  <img src="https://codecov.io/gh/nickatnight/py-clubhouse/branch/master/graph/badge.svg?token=E03I4QK6D9"/>\n</a>\n<a href="https://github.com/nickatnight/py-clubhouse/releases"><img alt="Actions Status" src="https://img.shields.io/pypi/v/py-clubhouse?style=plastic"></a>\n</p>\n\n\nPython client for Clubhouse (fork of [clubhouse-client](https://github.com/allardbrain/clubhouse-client) because I needed more flexibility for special use cases on work engagements)\n\n## Installation\n\nThe package is available on [pypi](https://pypi.org/project/py-clubhouse/) and can be installed like any other packages.\n\n    $ pip install py-clubhouse\n\n## Usage\n\nRefer to [Clubhouse API Docs](https://clubhouse.io/api/rest/v3/) for more information.\n\n```python\nfrom py_clubhouse import Clubhouse\n\nclubhouse = Clubhouse(\'your api key\')\n\nstory = clubhouse.get_story(1234)  # returns Story object\nworkflows = clubhouse.workflows()  # returns list of Workflow objects\n```\n\n## TODO\n* ~~add GHA workflow~~\n* create models for relevant resources\n* moar tests\n',
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
