import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR: Path = Path(__file__).parent.parent

load_dotenv(BASE_DIR / ".env")

API_TOKEN: str = os.getenv('API_TOKEN')
REDIS_SOCKET: str = os.getenv('REDIS_SOCKET')
REDIS_DB: str = os.getenv('REDIS_DB')
