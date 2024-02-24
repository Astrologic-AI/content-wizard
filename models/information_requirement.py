from pydantic import BaseModel


class InformationRequirement(BaseModel):
    key: str
    prompt: str
    validation: str  # Regex or other validation criteria
    required: bool = True
