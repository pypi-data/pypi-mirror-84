"""Python wrapper around the Zoom.us REST API
   Adapted from Patrick Schmid (prschmid/ zoomus) 
   Improved by Willy L W S"""

from __future__ import absolute_import, unicode_literals

from pw_zoomus.client import ZoomClient
from pw_zoomus.util import API_VERSION_1, API_VERSION_2


__all__ = ["API_VERSION_1", "API_VERSION_2", "ZoomClient"]
__version__ = "1.0.2"
