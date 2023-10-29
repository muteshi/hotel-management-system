import os
from dotenv import load_dotenv


load_dotenv()

secret_key = os.environ.get('SECRET_KEY')
