"""
TeleBridge settings.

This file automatically imports the appropriate settings based on the environment.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Check if we're in production or development
# You can set DJANGO_ENV=production in your environment to force production settings
DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development')

if DJANGO_ENV == 'production':
    # Production settings
    from .settings.production import *
else:
    # Development settings (default)
    from .settings.development import *
