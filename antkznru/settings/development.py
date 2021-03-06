# coding=utf-8
# Based on https://github.com/wooyek/cookiecutter-django-website by Janusz Skonieczny
"""
These should mimic a production settings making minimal modifications to accommodate development
"""

import logging
import os
import sys
from pathlib import Path

import environ

logging.basicConfig(format='%(asctime)s %(levelname)-7s %(thread)-5d %(filename)s:%(lineno)s | %(funcName)s | %(message)s', datefmt='%H:%M:%S')
logging.getLogger().setLevel(logging.DEBUG)
logging.disable(logging.NOTSET)
logging.getLogger('environ').setLevel(logging.INFO)
logging.debug("Settings loading: %s" % __file__)

name = __name__.split('.')[-1].upper()
print("""
╭─────────{border}──────────╮
│ Loading {name} settings │
╰─────────{border}──────────╯
""".format(name=name, border='─' * len(name)), file=sys.stderr)

# This will read missing environment variables from a file
# We want to do this before loading any base settings as they may depend on environment
environment_config = Path(__file__).with_suffix('.env')
if environment_config.exists():
    environ.Env.read_env(str(environment_config))

# noinspection PyUnresolvedReferences
from .base import *

# if 'DATABASE_URL' not in os.environ:
    # This a default fallback for local development and testing
    # BASE_DIR = Path(__file__).parents[2]
    # os.environ['DATABASE_URL'] = 'sqlite:///' + str(BASE_DIR / 'data' / 'db.dev.sqlite3')
    # os.environ['DATABASE_TEST_NAME'] = 'sqlite:///' + str(BASE_DIR / 'data' / 'db.tests.sqlite3')

