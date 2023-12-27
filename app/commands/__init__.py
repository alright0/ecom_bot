from app.commands.base_command import BaseCommand, SimpleCommand
from app.commands.command_calculation_request import CommandCalcRequest
from app.commands.command_faq import CommandFaq
from app.commands.command_show_cources_list import CommandShowCources
from app.commands.command_start import CommandStart

COMMANDS = [
    CommandStart,
    CommandCalcRequest,
    CommandShowCources,
    CommandFaq,
]

# сортируем по названию команды
COMMANDS.sort(key=lambda x: x.COMMANDS[0])
