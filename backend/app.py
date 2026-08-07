
"""
I think it would be better now to create a full JWT auth, 
I would need to make sure the ChatRequest has a concept of a student and 
I would have to redesign the generate_response function 
I need to ensure that depending on the exception error thrown which is worth a retry 
logged and a student coding error would be based in sandbox that will run their code and 
if they pass it will increase a rating on their coding skills and understanding of dsa but 
if they faill it would count as an attempt and Echo can get 
involved to help these are alot of implementations one that i never really thought about
"""


# Import FastAPI framework
from fastapi import FastAPI,HTTPException,status
#Imports a generated response to user
from backend.ai_service import generate_response
from backend.models import ChatRequest, ChatResponse, SubmissionRequest
from backend.sandbox import run_code, SandboxExecutionTimeout
from backend.expected_outputs import problems



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

@app.post("/submit")
def submission(request: SubmissionRequest):
  
    if request.user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Missing/Incorrect authentication credentials")  
    user_code = request.code

    problemId = request.problem_id

    if problemId not in problems:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    try:
        submission= run_code(code_to_run= user_code)
        decoded_submission = submission.output.decode("utf-8")
        is_correct = decoded_submission.strip() == problems[problemId]["expected"]
        return{
            "output": decoded_submission,
            "correct": is_correct,
            "exit_code": submission.exit_code
        }
    except SandboxExecutionTimeout as e:
        return{
            "timeout": f"Runtime Error in Sandbox {e}"
        }

    
# Chat endpoint
# Receives user messages from robot or website
@app.post("/chat")
async def chat(request: ChatRequest):
     
     if request.user_id is None:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                             detail="Missing/Incorrect authentication credentials")


    # Extract message from incoming request
     return ChatResponse(reply= await generate_response(request.message), expression= "neutral")


if __name__ =="__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
