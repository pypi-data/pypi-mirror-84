![PyPI - Downloads](https://img.shields.io/pypi/dm/GrailSort)
![PyPI - License](https://img.shields.io/pypi/l/GrailSort)
![Libraries.io SourceRank](https://img.shields.io/librariesio/sourcerank/pypi/GrailSort?color=green)
![PyPI](https://img.shields.io/pypi/v/GrailSort)
![PyPI - Format](https://img.shields.io/pypi/format/GrailSort)
![GitHub last commit](https://img.shields.io/github/last-commit/gaming32/grailsort)
<!-- ![PyPI - Status](https://img.shields.io/pypi/status/GrailSort) -->
<!-- ![Dependents (via libraries.io)](https://img.shields.io/librariesio/dependents/pypi/GrailSort) -->


# GrailSort for Python

GrailSort for Python is a Python API for the [GrailSort algorithm](https://github.com/Mrrl/GrailSort).

## Installation

You can install GrailSort for Python from source:
```shell
$ git clone https://github.com/gaming32/grailsort
$ cd grailsort
$ python setup.py install
```

Or you can install it from PyPI:
```shell
$ python -m pip install GrailSort
```

## Usage

GrailSort for Python comes with two modules: a strict one, and a slower one. The strict module (`cGrailSort`) only deals with `array.array('d')` objects, while the slower module (`grailsort`) deals with any Python sequence that contains comparable objects.
It is generally unnescessary to deal with the `grailsort` module, as you might as well use the built-in `list.sort` method or the `sorted` function. However, TimSort is not in-place, while GrailSort is. `cGrailSort` is useful when you need to sort with speed.

## Example

### grailsort

```python
import grailsort
import random

def print_out_of_order_index():
    index = next((i for i in range(len(l) - 1) if l[i] > l[i + 1]), None)
    print('Out of order index:', index)

l = list(range(1024))
print_out_of_order_index()

random.shuffle(l)
print_out_of_order_index()

grailsort.grailsort(l)
print_out_of_order_index()
```

### cGrailSort

```python
import cGrailSort
import array
import random

def print_out_of_order_index():
    index = next((i for i in range(len(a) - 1) if a[i] > a[i + 1]), None)
    print('Out of order index:', index)

a = array.array('d', range(1024))
print_out_of_order_index()

random.shuffle(a)
print_out_of_order_index()

cGrailSort.grailsort(a)
print_out_of_order_index()
```
