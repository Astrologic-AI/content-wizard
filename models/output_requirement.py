from typing import Optional

from pydantic import BaseModel


class OutputRequirement(BaseModel):
    key: str
    description: str
    validation: str  # Regex or other validation criteria
    required: bool = True
    default: Optional[str] = None
