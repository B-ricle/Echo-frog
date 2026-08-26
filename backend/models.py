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

Password = Annotated[
    str, 
    StringConstraints(
        strip_whitespace= True, 
        min_length = 8,
        max_length= 20,
    ),
]

Username = Annotated[
    str, 
    StringConstraints(
        strip_whitespace= True,
        min_length = 3,
        max_length = 20,
        pattern= r"^[a-zA-Z0-9_-]+$"
    )
]

# Define the expected structure of incoming chat requests
# The request must contain a message string
class ChatRequest(BaseModel):
    message: ChatMessage

class SubmissionRequest(BaseModel):
    code: str
    problem_id: int
        
class ChatResponse(BaseModel):
    reply: str
    expression: Literal["neutral"] = "neutral"

class SignupRequest(BaseModel):
    username: Username
    password: Password


class LoginRequest(BaseModel):
    username: Username
    password: Password
