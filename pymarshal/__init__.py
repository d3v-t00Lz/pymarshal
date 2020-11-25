"""
    Replicates the functionality of Golang's
    struct (un)marshalling feature to/from JSON.

    For examples, see:
    https://github.com/j3ffhubb/pymarshal/blob/master/README.md
"""

from . import json
from .json import *

__version__ = '2.0.2'
__all__ = json.__all__
