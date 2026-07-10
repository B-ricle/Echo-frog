import os
from pathlib import Path
from openai import AsyncOpenAI
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

#pulls the key from the env
api_key = os.getenv("OPEN_AI_KEY")

#Configures openai model and runs the gpt 5.4 mini model as back up
MODEL = os.getenv("OPENAI_MODEL" , "gpt-5.4-mini")

# Ensures that the key is found
if api_key is None:
    raise ValueError("OPEN_AI_KEY was not found. Check Echo-sec.env.")
else:
    print("OPEN_AI_KEY loaded successfully.")

#This is the general instructions Echo Frog will follow
ECHO_FROG_INSTRUCTIONS=(
            """
            You are Echo Frog, a friendly coding assistant and programming tutor.
            Help users understand programming, debugging, data structures, algorithms,
            software engineering, and related technical subjects.
            Adapt explanations to the user's experience level.
            Use accurate technical explanations along with simple everyday analogies
            or non-technical examples when they improve understanding.
            Define unfamiliar technical terms and provide code examples when useful.
            Be concise by default, but provide more detail when requested or necessary.
            Use a light frog personality without distracting from the answer.
            If you are uncertain, say so rather than inventing information.
            Do not claim to have performed physical actions.
            """
        )


#Assigns client to the openai key using a timeout as it controls approximately how long an OpenAI request attempt may wait before the SDK raises a timeout error
client = AsyncOpenAI(api_key=api_key, timeout=30.0, max_retries=1 )

# async so that the function can wait until the client responds 
async def generate_response(user_message: str) -> str:
    
    #await pauses the coroutine until OpenAI request completes, while allowing the loop to run other tasks 
    response = await client.responses.create(
        model=MODEL,
        input=user_message,
        instructions = ECHO_FROG_INSTRUCTIONS,
        max_output_tokens=500,

    )

    return response.output_text

