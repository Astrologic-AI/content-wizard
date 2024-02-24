from pydantic import BaseModel
from typing import List

from models.agent_profile import AgentProfile
from models.state import State


class ConversationConfig(BaseModel):
    name: str
    purpose: str
    final_output: str
    states: List[State]
    agent_profile: AgentProfile
    contextual_memory: List[str]  # Keys of information to remember throughout the conversation
