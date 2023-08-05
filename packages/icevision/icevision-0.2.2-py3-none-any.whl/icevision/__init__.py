from icevision.utils import *
from icevision.core import *
from icevision import parsers
from icevision import tfms
from icevision.data import *
from icevision import backbones
from icevision import models
from icevision.models import *
from icevision.metrics import *
from icevision.visualize import *

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__)
