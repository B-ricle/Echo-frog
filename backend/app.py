# Import FastAPI framework
from fastapi import FastAPI

# Import BaseModel for validating incoming request data
from pydantic import BaseModel


# Create the FastAPI application/server
app = FastAPI()


# Define the expected structure of incoming chat requests
# The request must contain a message string
class ChatRequest(BaseModel):
    message: str


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
def chat(request: ChatRequest):

    # Extract message from incoming request
    user_message = request.message

    # Return chatbot response
    return {
        "reply_text": f"Ribbit...you said: {user_message}",

        # Future expression system for frog emotions
        "expression": "neutral"
    }