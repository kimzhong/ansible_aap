from pydantic import BaseModel
from typing import Dict, Any

class RunPlaybookRequest(BaseModel):
    inventory: str | None = None
    extra_vars: Dict[str, Any] | None = None