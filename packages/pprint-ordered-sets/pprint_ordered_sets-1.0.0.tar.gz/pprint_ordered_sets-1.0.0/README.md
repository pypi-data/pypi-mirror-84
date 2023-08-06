# PPrint Ordered Sets
The standard library `pprint` module, but with the feature that
  all sets are ordered.

## Why does this package exist?
This package is a backport for the bug-fix [bpo-27495](https://bugs.python.org/issue27495).
This package ensures that `set` and `frozenset` objects are always ordered, which
  is not true of the `pprint` module.

As of writing this, the [pull request that fixes this bug](https://github.com/python/cpython/pull/22977)
  has not been merged.

## Example
```python
>>> import pprint_ordered_sets as pprint
>>> obj = set("abcdefg")
>>> print(obj)  # Will be different on different systems.
{'d', 'f', 'b', 'g', 'e', 'a', 'c'}
>>> pprint.pp(obj)  # Will be same on all systems.
{'a', 'b', 'c', 'd', 'e', 'f', 'g'}
```

## License
This code is licensed under the Python Software Foundation license, as this
  is a derivative work. My changes are adding the default ordering of `set` and
  `frozenset` objects, writing additional tests to cover these features, and renaming
  of this module to `pprint_ordered_sets`.

## Testing
This package requires no dependencies to test, simply run:
```bash
python -m unittest test_pprint_ordered_sets.py
```
