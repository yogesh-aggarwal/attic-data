import os

from dotenv import load_dotenv

load_dotenv()

# Environment variables

MONGO_URI = os.getenv("MONGO_URI")
