from app.commands.base_command import BaseCommand, SimpleCommand
from app.commands.command_calculation_request import CommandCalcRequest
from app.commands.command_payment_exapmle import CommandPaymentExample
from app.commands.command_start import CommandStart

COMMANDS = [
    CommandStart,
    CommandPaymentExample,
    CommandCalcRequest,
]

# сортируем по названию команды
COMMANDS.sort(key=lambda x: x.COMMANDS[0])
