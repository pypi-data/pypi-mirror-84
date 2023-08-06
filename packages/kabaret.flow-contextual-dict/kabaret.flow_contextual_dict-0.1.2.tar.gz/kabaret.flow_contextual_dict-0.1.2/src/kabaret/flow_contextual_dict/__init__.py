from __future__ import print_function

from .objects import ContextualView, get_contextual_dict

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
