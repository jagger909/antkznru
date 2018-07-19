# coding=utf-8
# Created 2014 by Janusz Skonieczny

"""
These are production settings, secrets should be loaded of the environment.

The goal here is to not change any settings may have impact on features present.
Changing keys and secrets should not have that impact.
"""

import logging
import os
import sys
from pathlib import Path

import environ


logging.basicConfig(format='%(asctime)s %(levelname)-7s %(thread)-5d %(filename)s:%(lineno)s | %(funcName)s | %(message)s', datefmt='%H:%M:%S')
logging.getLogger().setLevel(logging.DEBUG)
logging.disable(logging.NOTSET)

logging.debug("Settings loading: %s" % __file__)

name = __name__.split('.')[-1].upper()
print("""
╔═════════════════════════════╗
║ LOADING PRODUCTION SETTINGS ║
╚═════════════════════════════╝
""", file=sys.stderr)

# Set defaults for when env file is not present.
os.environ.update(DEBUG='False', ASSETS_DEBUG='False')

# This will read missing environment variables from a file
# We want to do this before loading any base settings as they may depend on environment
environment_config = Path(__file__).with_suffix('.env')
if environment_config.exists():
    environ.Env.read_env(str(environment_config))

# noinspection PyUnresolvedReferences
from .base import *

DATABASES['default']['OPTIONS'] = {
    'sslmode': 'require',
}

LOGGING['handlers']['console']['formatter'] = 'heroku'
LOGGING['handlers']['file'] = {
    'class': 'logging.handlers.RotatingFileHandler',
    'formatter': 'verbose',
    'backupCount': 3,
    'maxBytes': 4194304,  # 4MB
    'level': 'DEBUG',
    'filename': os.path.join(BASE_DIR , 'logs', 'website.log'),
}
LOGGING['root']['handlers'].append('file')

log_file = Path(LOGGING['handlers']['file']['filename'])
if not log_file.parent.exists():  # pragma: no cover
    logging.info("Creating log directory: {}".format(log_file.parent))
    Path(log_file).parent.mkdir(parents=True)
