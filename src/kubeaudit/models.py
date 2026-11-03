from dataclasses import dataclass
from enum import Enum

class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

@dataclass
class Finding:
    check_id: str
    severity: Severity
    kind: str
    namespace: str
    name: str
    message: str