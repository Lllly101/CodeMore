[TOC]

### Module search path

*sys.path* is composed of four component：

### Relative Import

```python
from . import spam
```

In 2.X, the leading dot import will still default to the original *relative-then-
absolute* search path order.

### No request in module urllib

Import usage demo

```bash
>>> import urllib
>>> urllib.request.getproxies()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: module 'urllib' has no attribute 'request'
```

Correct usage

```bash
>>> import urllib.request
```

### Differences between Python2.x and Python3.X

#### Byte code files storage

In Python 3.2 and later—
byte code files are segregated in a `__pycache__` subdirectory and named with their
Python version to avoid contention and recompiles when multiple Pythons are
installed.

