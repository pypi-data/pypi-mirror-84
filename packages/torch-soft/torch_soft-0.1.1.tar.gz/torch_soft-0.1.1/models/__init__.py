# from os.path import dirname, basename, isfile, join
# import glob
# modules = glob.glob(join(dirname(__file__), "*.py"))
# __all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

from .networks import *
from .resnet import *
from .quiz_dnn import *
from .assignment11 import *
from.naiveresnet import *