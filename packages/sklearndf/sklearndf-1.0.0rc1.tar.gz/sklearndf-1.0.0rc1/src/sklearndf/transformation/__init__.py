"""
Extended versions of all Scikit-Learn transformers with enhanced E2E support for data
frames.
"""
from packaging.version import parse as __parse_version
from sklearn import __version__ as __sklearn_version__

from ._transformation import *

if __parse_version(__sklearn_version__) >= __parse_version("0.22"):
    from ._transformation_v0_22 import *

if __parse_version(__sklearn_version__) >= __parse_version("0.23"):
    from ._transformation_v0_23 import *
