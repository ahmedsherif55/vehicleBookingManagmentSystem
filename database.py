from services.mysql import Database
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')
db = Database(db_host=DATABASE_HOST, db_user=DATABASE_USER, db_password=DATABASE_PASSWORD, db_name=DATABASE_NAME)
