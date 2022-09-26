import time
from ..common.error import Result, Error


class SampleController:
    def get_systime(self) -> Result[str]:
        return time.strftime("%H:%M:%S"), None

    def returns_error(self) -> Result[str]:
        return "", Error(500, "Some Error")
