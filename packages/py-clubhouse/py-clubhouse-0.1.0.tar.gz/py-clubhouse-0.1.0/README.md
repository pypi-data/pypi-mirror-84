# py-clubhouse
Python client for Clubhouse (fork of [clubhouse-client](https://github.com/allardbrain/clubhouse-client) because I needed more flexibility for special use cases on work engagements)

## Installation

The package is available on [pypi](https://pypi.org/project/clubhouse/) and can
be installed like any other packages.

    $ pip install py-clubhouse

## Usage

Refer to [Clubhouse API Docs](https://clubhouse.io/api/rest/v3/) for more information.

```python
from py_clubhouse import Clubhouse

clubhouse = Clubhouse('your api key')

story = {'name': 'A new story', 'description': 'Do something!'}
clubhouse.post('stories', json=story)
```

## TODO
* create models for relevant resources
* moar tests
