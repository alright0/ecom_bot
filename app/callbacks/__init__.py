from typing import Any, List

from app.callbacks.base_callback import BaseCallback
from app.callbacks.callback_calculation_request import CallbackCalculationRequest

CALLBACKS: List[Any] = [
    CallbackCalculationRequest,
]
