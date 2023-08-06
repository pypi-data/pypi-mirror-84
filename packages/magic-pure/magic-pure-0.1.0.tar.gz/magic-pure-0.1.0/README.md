# magic-pure

`magic-pure` is a pure Python implementation. For the moment, it helps me to execute code which uses [`python-magic`](https://pypi.org/project/python-magic/) on Windows.

Maybe, at some point, it can be used as a drop-in replacement.


## Installation

```
$ pip install magic-pure
```

## Usage

```python
>>> import magic
>>> magic.from_file("testdata/test.pdf")
'PDF document, version 1.2'
```
