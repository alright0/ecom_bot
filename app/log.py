import logging
import sys
from pathlib import Path
from typing import Any

from telebot.types import Message

from app.config import Config

LOGGER_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOGGER_DATE = "%d-%m-%y %H:%M:%S"


def create_logger(name: str, path: Path) -> None:
    """
    Создает логгер с указанным именем по указанному пути.

    :param name: Имя логгера
    :param path: Путь сохранения логгера
    """

    formatter = logging.Formatter(LOGGER_FORMAT, LOGGER_DATE)

    handler = logging.FileHandler(path / f"{name}.log")
    handler.setLevel(logging.DEBUG)
    handler.name = name
    handler.setFormatter(formatter)
    handler.encoding = "utf-8"

    logger = logging.getLogger(name)
    logger.addHandler(handler)


def init_logging(config: Config) -> None:
    """
    Инициализирует логи.

    :param config: Класс конфигурации бота
    """

    path = config.logs_path
    logging.basicConfig(
        filename=path / "app.log",
        filemode="a",
        level=logging.NOTSET,
        format=LOGGER_FORMAT,
        datefmt=LOGGER_DATE,
        encoding="utf-8",
    )
    logging.raiseExceptions = False
    create_logger("manual", path)
    create_logger("messages", path)
    create_logger("sqlalchemy", path)
    if not config.testing:
        sys.stderr = open(path / "stderr.log", "a", encoding="utf-8")


def manual_log(
    message: Message,
    logger: logging.Logger = logging.getLogger("manual"),
    **kwargs: dict,
) -> None:
    """
    Создает запись лога сообщения с основными данными сообщения и дополнительными аргументами.

    :param message: Тг-сообщение
    :param logger: Логгер
    :param kwargs: Дополнительные агрументы
    """

    kwargs_str = "".join([f"{k}: {v} " for k, v in kwargs.items()])
    log_str = (
        f"{message.chat.id} {message.chat.username} "
        f"{message.chat.first_name} {message.chat.last_name} "
        f"text: {message.text}. " + kwargs_str
    ).replace("\n", " ")

    logger.info(log_str)


def get_kwarg_str(data: dict, key: Any) -> str:
    """
    Получает значения ключа и отдает его в подходящей для лога форме.

    :param data: Словарь
    :param key: Ключ
    :return: строка в формате 'key: value'
    """
    text = data.get(key, "")
    return f"{key}: {text} " if text else ""
