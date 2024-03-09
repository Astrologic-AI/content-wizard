from pydantic import BaseModel
from typing import List, Optional

from models.information_requirement import InformationRequirement


class State(BaseModel):
    name: str
    description: str
    information_requirements: List[InformationRequirement]
    next_state_criteria: Optional[str]  # Logic or condition for transitioning to the next state
