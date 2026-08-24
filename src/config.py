"""
Configuration management for GitTrack.
"""

import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for GitTrack"""
    
    # GitLab
    GITLAB_TOKEN = os.getenv('GITLAB_TOKEN', 'mock_token')
    GITLAB_PROJECT_ID = os.getenv('GITLAB_PROJECT_ID', '123456')
    GITLAB_URL = os.getenv('GITLAB_URL', 'https://gitlab.com')
    USE_MOCK_DATA = os.getenv('USE_MOCK_DATA', 'True').lower() == 'true'
    
    # GitHub
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
    GITHUB_REPO = os.getenv('GITHUB_REPO', '')
    
    # AWS
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    
    # App
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.USE_MOCK_DATA and not cls.GITLAB_TOKEN:
            raise ValueError("GITLAB_TOKEN required when USE_MOCK_DATA=False")
        return True

# Create a config instance
config = Config()

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Validate configuration
try:
    config.validate()
except ValueError as e:
    print(f"⚠️  Configuration Warning: {e}")
    print("Please set required variables in .env file")
