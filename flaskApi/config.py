#!/usr/bin/env python

import os 
from dotenv import load_dotenv
load_dotenv()


class Config:
    """
    Base configuration class. Contains default configuration settings + configuration settings applicable to all environments.
    """
    # Default settings
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    # Settings applicable to all environments
    SECRET_KEY = os.getenv(
        'SECRET_KEY', default='who know what is the acctual value is 🔓️ ?')
    
    

class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    FLASK_ENV = 'production'



