from typing import Any, Dict, Optional
from pydantic import BaseModel


class IntentInput(BaseModel):
    text: str
    language: Optional[str] = "en"


class IntentResult(BaseModel):
    intent: str
    entities: Dict[str, Any] = {}
    confidence: Optional[float] = None


class ExecuteRequest(BaseModel):
    user_id: str
    intent: str
    amount: Optional[float] = None
    recipient: Optional[str] = None


class CommandResult(BaseModel):
    success: bool
    message: str
    data: Dict[str, Any] = {}
