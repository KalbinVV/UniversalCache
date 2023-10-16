import datetime
from dataclasses import dataclass
from typing import Any


@dataclass
class CacheTTLValuePair:
    expire_time: datetime.datetime
    value: Any
