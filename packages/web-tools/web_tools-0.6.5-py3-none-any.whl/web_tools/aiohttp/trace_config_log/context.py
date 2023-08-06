from __future__ import annotations

import copy
import datetime
from typing import Dict, Optional


class LogContext:
    request_datetime: datetime.datetime
    request_url: str
    request_method: str
    request_headers: Dict[str, str]
    request_body: bytes

    response_datetime: datetime.datetime
    response_status_code: Optional[int]
    response_headers: Optional[Dict[str, str]]
    response_body: Optional[bytes]

    elapsed_time: datetime.timedelta
    exception: Optional[str]

    @classmethod
    def create_context(cls, trace_request_ctx=None) -> LogContext:
        instance = cls()
        return instance

    def as_dict(self) -> Dict:
        return copy.copy(self.__dict__)
