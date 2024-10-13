import os

from dotenv import load_dotenv

load_dotenv()

# Runtime constants

THREAD_POOL_MAX_WORKERS = 32

# Environment variables

MONGO_URI = os.getenv("MONGO_URI")
assert MONGO_URI, "MONGO_URI is not set"
