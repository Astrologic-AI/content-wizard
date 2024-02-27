from pydantic import BaseModel
from typing import List

from models.agent_profile import AgentProfile
from models.output_requirement import OutputRequirement
from models.state import State


class ConversationConfig(BaseModel):
    name: str
    purpose: str
    agent_profile: AgentProfile
    states: List[State]
    output: List[OutputRequirement]
