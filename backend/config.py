import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', False)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# DeepSeek API
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_MODEL = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
DEEPSEEK_API_URL = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1')

# QiChacha
QICHACHA_API_KEY = os.getenv('QICHACHA_API_KEY')
QICHACHA_API_URL = os.getenv('QICHACHA_API_URL', 'https://api.qichacha.com')

# News API
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_URL = os.getenv('NEWS_API_URL', 'https://newsapi.org/v2')
