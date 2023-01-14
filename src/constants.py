import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR: Path = Path(__file__).parent.parent

load_dotenv(BASE_DIR / ".env")

API_TOKEN: str = os.getenv('API_TOKEN')

REDIS_SOCKET: str = os.getenv('REDIS_SOCKET')
REDIS_DB: int = int(os.getenv('REDIS_DB'))
REDIS_DB_FSM: int = int(os.getenv('REDIS_DB_FSM'))

SECRET_KEYS: list = os.getenv('SECRET_KEYS').split("\n")[1:]
