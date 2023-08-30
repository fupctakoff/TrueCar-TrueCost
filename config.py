import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY=os.environ.get('SECRET_KEY')
DB_NAME=os.environ.get('DB_NAME')
DB_USER=os.environ.get('DB_USER')
DB_PASSWORD=os.environ.get('DB_PASSWORD')
DB_HOST=os.environ.get('DB_HOST')
REDIS_LOCATION=os.environ.get('REDIS_LOCATION')
