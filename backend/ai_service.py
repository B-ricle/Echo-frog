import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / "Echo-sec.env"

load_dotenv(ENV_PATH)

#pulls the key from the env
api_key = os.getenv("OPEN_AI_KEY")

# Pulls the key from the env
api_key = os.getenv("OPEN_AI_KEY")

# Ensures that the key is found
if api_key is None:
    raise ValueError("OPEN_AI_KEY was not found. Check Echo-sec.env.")
else:
    print("OPEN_AI_KEY loaded successfully.")

#Assigns client to the openai key
client = OpenAI(api_key=api_key)

def generate_response(user_message):
    
    response = client.responses.create(
        model= "gpt-5.4-mini",
        input = user_message

    )

    return response.output_text

