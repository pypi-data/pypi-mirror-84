from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Mail:
    to: List[str]
    subject: str
    body: str
    cc: List[str] = field(default_factory=list)
    bcc: List[str] = field(default_factory=list)
    headers: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for attr in ["to", "cc", "bcc"]:
            value = getattr(self, attr)
            if isinstance(value, str):
                setattr(self, attr, [value])
