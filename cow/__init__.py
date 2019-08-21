import os
import sys

from .text_generate import generate_permutation
from .cache import create_disk_cache
from .curl_util import execute_curl
from .debug import is_debug, is_docker
from .dict_utils import remove_key_except, md5
from .function_util import timing, ignore_exception
from .lazy_load import LazyProperty
from .logging_util import LogBuilder
from .notification import notify_message
from .path_util import ensure_directory_exists
from .rsa_encrpyt_helper import RSAEncryptHelper
from .string_util import keymap_replace
from .time_utils import get_ntp_time
from .webservice_util import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/patterns/observer")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/patterns/singleton")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/patterns/visitor")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/patterns/service_registry")
