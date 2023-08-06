# py-clubhouse

<p align="center">
<a href="https://github.com/nickatnight/py-clubhouse"><img alt="Build Status" src="https://github.com/nickatnight/py-clubhouse/workflows/Run%20CI/badge.svg?branch=master"></a>
<a href="https://codecov.io/gh/nickatnight/py-clubhouse">
  <img src="https://codecov.io/gh/nickatnight/py-clubhouse/branch/master/graph/badge.svg?token=E03I4QK6D9"/>
</a>
<a href="https://pypi.org/project/py-clubhouse/"><img alt="Actions Status" src="https://img.shields.io/pypi/v/py-clubhouse?style=plastic"></a>
</p>


Python client for Clubhouse (started as a fork of [clubhouse-client](https://github.com/allardbrain/clubhouse-client))

## Installation

The package is available on [pypi](https://pypi.org/project/py-clubhouse/) and can be installed like any other packages.

    $ pip install py-clubhouse

## Usage

Refer to [Clubhouse API Docs](https://clubhouse.io/api/rest/v3/) for more information.

```python
from py_clubhouse import Clubhouse

clubhouse = Clubhouse('your api key')

story = clubhouse.get_story(1234)  # returns Story object
workflows = clubhouse.workflows()  # returns list of Workflow objects
stories = clubhouse.search_stories("state:Staging")  # returns list of Story objects
```

## Development

1. Clone repo
2. Install [poetry](https://github.com/python-poetry/poetry/blob/master/README.md) globally.
3. Activate virtual env `poetry shell`
4. Install dependencies with `poetry install`
5. Run pytest `poetry run pytest`

## TODO

* ~~add GHA workflow~~
* ~~create models for relevant resources~~
* moar tests
* add c.r.u.d. methods for relevant models
