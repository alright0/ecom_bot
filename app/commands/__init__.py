from app.commands.base_command import BaseCommand, SimpleCommand
from app.commands.command_start import CommandStart

COMMANDS = [
    CommandStart,
]

# сортируем по названию команды
COMMANDS.sort(key=lambda x: x.COMMANDS[0])
