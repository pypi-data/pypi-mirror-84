# py-clubhouse

<p align="center">
<a href="https://codecov.io/gh/nickatnight/py-clubhouse">
  <img src="https://codecov.io/gh/nickatnight/py-clubhouse/branch/master/graph/badge.svg?token=E03I4QK6D9"/>
</a>
<a href="https://github.com/nickatnight/py-clubhouse/releases"><img alt="Actions Status" src="https://img.shields.io/pypi/v/py-clubhouse?style=plastic"></a>
</p>


Python client for Clubhouse (fork of [clubhouse-client](https://github.com/allardbrain/clubhouse-client) because I needed more flexibility for special use cases on work engagements)

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
```

## TODO
* ~~add GHA workflow~~
* create models for relevant resources
* moar tests
