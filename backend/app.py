# Import FastAPI framework
from fastapi import FastAPI
#Imports a generated response to user
from ai_service import generate_response
from models import ChatRequest, ChatResponse


# Create the FastAPI application/server
app = FastAPI()

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
     return ChatResponse(reply= await generate_response(request.message), expression= "neutral")

if __name__ =="__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
