import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()


class Config:
    token = os.getenv("TOKEN", "")
    payment_token = os.getenv("PAYMENT_TOKEN", "")

    bot_id = None  # инициализируем в боте
    log_chat = os.getenv("LOG_CHAT")
    testing = int(os.getenv("TESTING", 0))
    owner = int(os.getenv("OWNER", 0))

    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "db")
    port = os.getenv("POSTGRES_PORT", "")
    db = os.getenv("POSTGRES_DB", "tg_bot")

    db_url = f"postgresql://{user}:{password}@{server}:{port}/{db}"

    path = Path(__file__).parents[0]
    media_path = path.parents[0] / "media"
    logs_path = path.parents[0] / "logs"

    redis_url = os.getenv("REDIS_URL")

    state = {"horoscope_period": "today"}

    def set_state(self, key: Any, value: Any) -> None:
        self.state[str(key)] = value

    def get_state(self, key: Any, default: Any = None) -> Any:
        return self.state.get(str(key), default)


config = Config()
