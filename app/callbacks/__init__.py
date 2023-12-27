from typing import Any, List

from app.callbacks.base_callback import BaseCallback
from app.callbacks.callback_calculation_request import CallbackCalculationRequest
from app.callbacks.callback_return_paid_course import CallbackReturnPaidCourse
from app.callbacks.callback_send_course_invoice import CallbackSendCourceInvoice

CALLBACKS: List[Any] = [
    CallbackCalculationRequest,
    CallbackReturnPaidCourse,
    CallbackSendCourceInvoice,
]
