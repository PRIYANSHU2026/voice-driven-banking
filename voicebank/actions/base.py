from abc import ABC, abstractmethod
from typing import Dict, Any
from voicebank.models import CommandResult


class ActionExecutor(ABC):
    @abstractmethod
    def execute(self, action: str, params: Dict[str, Any]) -> CommandResult:
        raise NotImplementedError
