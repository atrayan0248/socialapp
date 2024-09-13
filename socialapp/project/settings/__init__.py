from __future__ import annotations

import os.path
from pathlib import Path

from pymongo import MongoClient
from split_settings.tools import include
from split_settings.tools import optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Namespacing custom environment variable prefix
ENVVAR_SETTINGS_PREFIX = 'SOCIALAPP_'

# Local Developer Settings file from environment variable
LOCAL_SETTINGS_PATH = os.getenv(f'{ENVVAR_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH')

if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = 'local/settings.dev.py'

if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)

include('base.py', 'logging.py', 'custom.py', optional(LOCAL_SETTINGS_PATH), 'envvars.py', 'docker.py')

# MongoDB Connection Parameters
MONGO_DB_URL = 'mongodb://localhost:27017'

# Create a MongoClient to the Mongo Instance
client = MongoClient(MONGO_DB_URL)

# Select the database to be used
DB = client['socialapp-db']
