from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DB_URL")
UPLOAD_DIR = os.getenv("UPLOAD_DIR")
JWT_EXPIRATION_TIME = os.getenv("JWT_EXPIRATION_TIME")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")