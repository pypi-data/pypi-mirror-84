"""
FSlash (F/) aims to be a solid library for practical functional programming in
Python 3.8+ inspired by [F#](https://fsharp.org). By practical we mean that the
goal of the library if to enable you to do meaningful and productive functional
programming in Python instead of being a [Monad
tutorial](https://github.com/dbrattli/OSlash).

GitHub: https://github.com/dbrattli/FSlash
"""

from . import builder as ce
from . import collections, core

__all__ = ["core", "collections", "ce"]

from ._version import get_versions

__version__ = get_versions()["version"]  # type: ignore
del get_versions
