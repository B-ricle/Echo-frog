# Import FastAPI framework
from fastapi import FastAPI

# Import BaseModel for validating incoming request data
from pydantic import BaseModel, field_validator
#Imports a generated response to user
from backend.ai_service import generate_response


# Create the FastAPI application/server
app = FastAPI()

 

# Define the expected structure of incoming chat requests
# The request must contain a message string
class ChatRequest(BaseModel):
    message: str
    @field_validator("message")
    @classmethod
    def validate_message(cls, message: str) -> str:
        cleaned_message = message.strip()
        if not cleaned_message:
            raise ValueError("The message cannot be empty.")
        if len(cleaned_message) > 4000:
            raise ValueError("Message cannot exceed 4,000 characters.")
        return cleaned_message
            


# Root route
# Used to confirm that the backend is online
@app.get("/")
def home():

    # Return JSON response
    return {
        "status": "EchoFrog Backend online"
    }


# Chat endpoint
# Receives user messages from robot or website
@app.post("/chat")
async def chat(request: ChatRequest):

    # Extract message from incoming request
    user_message = request.message
    ai_reply = await generate_response(request.message)

    # Return chatbot response
    return {
        # Future expression system for frog emotions
        "expression": request.message,
        "reply text": ai_reply
        
    }
    

