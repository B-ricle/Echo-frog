
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
from backend.database import get_connection




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

    with get_connection() as connect:
        with connect.cursor() as cursor:
            cursor.execute("SELECT expected_output FROM problems WHERE id=%s" , (problemId,))

            result= cursor.fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="Problem not found")

    expected_output = result[0]

    try:
        submission= run_code(code_to_run= user_code)

        is_correct = submission.output.strip() == expected_output.strip()

        if submission.exit_code != 0:
            outcome = 'runtime_error'
        elif is_correct:
            outcome = 'passed'
        else:
            outcome = 'wrong_answer'

        exit_code = submission.exit_code
        submission_duration = submission.duration_exec
        output = submission.output

    except SandboxExecutionTimeout:
        outcome = 'timeout'
        exit_code = None 
        submission_duration = 5.0
        output = ''
        is_correct = False

    with get_connection() as connect:
        with connect.cursor() as cursor:

            cursor.execute(
            """
            INSERT INTO attempts(student_id, problem_id, code, outcome, exit_code, duration) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """, 
            (request.user_id, problemId, user_code, outcome, exit_code, submission_duration)
            )
            connect.commit()
            
    return {
        "outcome": outcome,
        "exit_code": exit_code,
        "duration": submission_duration,
        "output": output,
        "is_correct": is_correct
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
