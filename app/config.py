import os

def read_secret(secret_name):
    """Read the secret value from the specified file."""
    secret_path = f'/run/secrets/{secret_name}'
    try:
        with open(secret_path, 'r') as secret_file:
            return secret_file.read().strip()
    except FileNotFoundError:
        # Fallback to environment variable if secret file is not found
        return os.getenv(secret_name.upper(), 'dev_secret')

class Config:
    DEBUG = True  # Change to False in production
    SECRET_KEY = read_secret('secret_key')
    
    # Database credentials
    POSTGRES_USER = read_secret('postgres_user')
    POSTGRES_PASSWORD = read_secret('postgres_password')
    POSTGRES_DB = read_secret('postgres_db')
    
    # Database URI
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Logging configuration
    LOGGING_LEVEL = 'DEBUG'
