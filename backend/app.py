from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

#Retrieves the 
@app.get("/")
def home():
    return {"status": "EchoFrog Backend online"
    }

@app.post("/chat")
def chat(request: ChatRequest):
    user_message = request.message
    return{
    "reply_text": f"Ribbit...you said: {user_message}",
    "expression" : "neutral"

}

@app.get("/health")
def healthcheck():
    return{
        "status": "ok",
        "service": "EchoFrog Backend"
    }