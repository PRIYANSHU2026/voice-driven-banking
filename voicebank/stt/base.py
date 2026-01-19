from abc import ABC, abstractmethod
from typing import Optional


class SpeechToText(ABC):
    @abstractmethod
    def transcribe(self, audio_bytes: bytes, language: Optional[str] = "en") -> str:
        raise NotImplementedError
