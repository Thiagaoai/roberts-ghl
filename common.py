from dataclasses import dataclass
from typing import Any


@dataclass
class StepResult:
    step: str
    status: str
    detail: str
    data: dict[str, Any] | None = None

    def as_dict(self) -> dict[str, Any]:
        payload = {
            "step": self.step,
            "status": self.status,
            "detail": self.detail,
        }
        if self.data:
            payload["data"] = self.data
        return payload
