"""
TeleBridge settings.

This file imports the appropriate settings based on the environment.
"""

import os

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telebridge.settings.development')

# Import the appropriate settings
from .settings.development import *
