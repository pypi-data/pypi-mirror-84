"""Top-level package of rna."""

__author__ = """Daniel Böckenhoff"""
__email__ = "dboe@ipp.mpg.de"
__version__ = "0.6.2"

from . import plotting
from . import log  # NOQA
from . import path  # NOQA

plotting.use("matplotlib")
