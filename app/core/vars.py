from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DB_URL")
UPLOAD_DIR = os.getenv("UPLOAD_DIR")

