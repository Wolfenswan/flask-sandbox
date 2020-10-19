"""
default config, move to /instance/
TODO if possible, check in app.py if instance/config exists and if not copy/move this file
"""

import os
import secrets

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(16)