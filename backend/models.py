from pydantic import BaseModel, StringConstraints
from typing import Annotated, Literal


ChatMessage = Annotated[
    str,
    StringConstraints(
        strip_whitespace= True,
        min_length= 1,
        max_length=4000,

    ),
]


# Define the expected structure of incoming chat requests
# The request must contain a message string
class ChatRequest(BaseModel):
    message: ChatMessage
    user_id: str | None = None

class SubmissionRequest(BaseModel):
    user_id: str | None = None
    code: str
    problem_id: str



         
class ChatResponse(BaseModel):
    reply: str
    expression: Literal["neutral"] = "neutral"
