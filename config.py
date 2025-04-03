import os
from dotenv import load_dotenv

load_dotenv()


class Config:
	# Database Configuration
	POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
	POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
	POSTGRES_DB = os.getenv('POSTGRES_DB', 'crawler_db')
	POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
	POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

	# SQLAlchemy Configuration
	SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Crawler Configuration
	TAGESSCHAU_BASE_URL = 'https://www.tagesschau.de'
	TAGESSCHAU_OVERVIEW_URL = 'https://www.tagesschau.de/news/'
	CRAWLER_INTERVAL = 60  # minutes