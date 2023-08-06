__version__ = "0.1.2"


import pathlib

import requests

from .api import *


config = None

def set_conf(filepath: str) -> dict:

  global config

  with open(filepath) as f:
    config = json.load(f)

  return config
