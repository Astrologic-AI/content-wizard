from typing import List

from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from pydantic import BaseModel


class AgentProfile(BaseModel):
    name: str
    description: str
    model: str
    prompt_template: PromptTemplate
    tools: List[Tool]
