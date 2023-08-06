# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pprint_ordered_sets']
setup_kwargs = {
    'name': 'pprint-ordered-sets',
    'version': '1.0.0',
    'description': 'The standard library pprint module, but sets are always ordered.',
    'long_description': '# PPrint Ordered Sets\nThe standard library `pprint` module, but with the feature that\n  all sets are ordered.\n\n## Why does this package exist?\nThis package is a backport for the bug-fix [bpo-27495](https://bugs.python.org/issue27495).\nThis package ensures that `set` and `frozenset` objects are always ordered, which\n  is not true of the `pprint` module.\n\nAs of writing this, the [pull request that fixes this bug](https://github.com/python/cpython/pull/22977)\n  has not been merged.\n\n## Example\n```python\n>>> import pprint_ordered_sets as pprint\n>>> obj = set("abcdefg")\n>>> print(obj)  # Will be different on different systems.\n{\'d\', \'f\', \'b\', \'g\', \'e\', \'a\', \'c\'}\n>>> pprint.pp(obj)  # Will be same on all systems.\n{\'a\', \'b\', \'c\', \'d\', \'e\', \'f\', \'g\'}\n```\n\n## License\nThis code is licensed under the Python Software Foundation license, as this\n  is a derivative work. My changes are adding the default ordering of `set` and\n  `frozenset` objects, writing additional tests to cover these features, and renaming\n  of this module to `pprint_ordered_sets`.\n\n## Testing\nThis package requires no dependencies to test, simply run:\n```bash\npython -m unittest test_pprint_ordered_sets.py\n```\n',
    'author': 'Ben Bonenfant',
    'author_email': 'bonenfan5ben@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bbonenfant/pprint_ordered_sets',
    'py_modules': modules,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
