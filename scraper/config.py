import os
from dotenv import load_dotenv

load_dotenv()

class Config: 

    APP_ID = os.getenv("APP_ID")
    APP_SECRET = os.getenv("APP_SECRET")
    APP_NAME = os.getenv("APP_NAME")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")

