# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_clubhouse', 'py_clubhouse.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'py-clubhouse',
    'version': '0.1.0',
    'description': 'Python client for Clubhouse',
    'long_description': "# py-clubhouse\nPython client for Clubhouse (fork of [clubhouse-client](https://github.com/allardbrain/clubhouse-client) because I needed more flexibility for special use cases on work engagements)\n\n## Installation\n\nThe package is available on [pypi](https://pypi.org/project/clubhouse/) and can\nbe installed like any other packages.\n\n    $ pip install py-clubhouse\n\n## Usage\n\nRefer to [Clubhouse API Docs](https://clubhouse.io/api/rest/v3/) for more information.\n\n```python\nfrom py_clubhouse import Clubhouse\n\nclubhouse = Clubhouse('your api key')\n\nstory = {'name': 'A new story', 'description': 'Do something!'}\nclubhouse.post('stories', json=story)\n```\n\n## TODO\n* create models for relevant resources\n* moar tests\n",
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
