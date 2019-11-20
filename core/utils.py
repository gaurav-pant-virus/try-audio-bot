import errno
import os
import pkgutil
import random
import re
import shutil
import string
from datetime import datetime, timedelta
from distutils import dir_util
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit


def get_module_attr(access_path):
    """
    This method will take complete access path as an argument and return requested object.
    """
    parts = access_path.split('.')
    module = ".".join(parts[:-1])
    obj = __import__(module)
    for comp in parts[1:]:
        obj = getattr(obj, comp)
    return obj
