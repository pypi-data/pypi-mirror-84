# evonik-dummy

This repo contains the python module `evonik.dummy`.
It is publically available on the python package index as the package `evonik-dummy`.

The module contains python classes to generate dummy data. These classes and their attributes / arguments are designed with the properties of data elements in [OpenAPI](https://swagger.io/specification/) in mind. They can be used to generate example data for testing and showcasing APIs, including REST and GQL.



## Repo Structure

```
evonik/            # source code of evonik-dummy
notebooks/         # jupyter notebooks with examples and doc
LICENSE            # MIT license file
README.md          # this README
setup.py           # pypi setup script
requirements.txt   # list of dependencies
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `evonik.dummy` as the package `evonik-dummy`.

```bash
pip install evonik-dummy
```

## Usage

```python
from evonik.dummy import String, Integer

print(String().valids(5))
print(Integer().invalids(exhaustive=True))
```

## Test

To test the current implementation, execute the following:

```
pytest evonik/dummy
```

## Build & Upload

To build the package and upload a new version to pypi, execute the following commands:

```
rm -rf build dist evonik_dummy.egg-info
python3 setup.py sdist bdist_wheel --universal
twine upload dist/*
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

