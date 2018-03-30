import sys

from .cache import *
from .config_base import ConfigBase
from .curl_util import *
from .debug import is_debug
from .dict_utils import *
from .function_util import *
from .logging_util import *
from .path_util import *
from .picklezip import *
from .string_util import *
from .try_catch_util import *
from .spare_array_zip import *
from .debug import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/patterns/observer")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/patterns/singleton")
