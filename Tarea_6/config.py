import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-local-de-desarrollo")

    KEYDB_HOST = os.getenv("KEYDB_HOST", "localhost")
    KEYDB_PORT = int(os.getenv("KEYDB_PORT", 6379))
    KEYDB_DB = int(os.getenv("KEYDB_DB", 0)
    )
