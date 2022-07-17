import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
DATABASE = os.getenv("DATABASE")
PASSWORD = os.getenv('PASSWORD')
