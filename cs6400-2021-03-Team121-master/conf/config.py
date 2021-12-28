import os

# =============================================================================
# APP Basic Settings
# =============================================================================
SERVICE_NAME = 'Jaunty Jalopies'
DEBUG = os.environ.get('DEBUG').lower() in ['true', 't', '1', 'y']
SECRET_KEY = os.environ.get("SECRET_KEY")
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
RESET_DB = os.environ.get('RESET_DB', 'True').lower() in ['t', 'true', 'y', 'yes', '1']

# =============================================================================
# DB settings
# =============================================================================
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get('DB_PORT', 5432)
DB_NAME = os.environ.get('DB_NAME')
DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

PUBLIC_ACCESS_RESOURCES = ['login', 'search', 'static']


