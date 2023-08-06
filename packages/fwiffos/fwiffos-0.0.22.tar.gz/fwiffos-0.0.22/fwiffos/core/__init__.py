# -*- coding: utf-8 -*-

name = 'core'
__version__ = "0.0.22"


def version():
    return __version__

from .core import Node
from .identity import NodeID 
from .log import log
