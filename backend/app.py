# Import FastAPI framework
from fastapi import FastAPI

# Import BaseModel for validating incoming request data
from pydantic import BaseModel, StringConstraints
#Imports a generated response to user
from backend.ai_service import generate_response

from typing import Annotated
# Literal means "only these exact values are accepted"
from typing import Literal


# Create the FastAPI application/server
app = FastAPI()


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
            
class ChatResponse(BaseModel):
    reply: str
    expression: Literal["neutral"] = "neutral"


# Root route
# Used to confirm that the backend is online
@app.get("/")
def home():

    # Return JSON response
    return {
        "status": "EchoFrog Backend online"
    }
# health check 
@app.get("/health")
def health():
    return{
        "status": "healthy"
    }
    
# Chat endpoint
# Receives user messages from robot or website
@app.post("/chat")
async def chat(request: ChatRequest):

    # Extract message from incoming request
    user_message = request.message
    ChatRequest =  await generate_response(request.message)

    # Return chatbot response
    return {
        ChatResponse   
    }
    

