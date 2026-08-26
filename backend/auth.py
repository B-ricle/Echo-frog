import bcrypt
import os 
import datetime
from dotenv import load_dotenv
from pathlib import Path
import jwt
script_dir = Path(__file__).resolve().parent.parent
ENV_PATH = script_dir / "Jwt_auth.env"

load_dotenv(ENV_PATH)

THEE_KEY = os.getenv("JWT_K")

class InvalidTokenError(Exception):

    pass


def hash_password(plain_password: str) -> str:
    password_bytes = plain_password.encode('utf-8')

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    return hashed_password.decode('utf-8')




def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')

    stored_hash_bytes = hashed_password.encode('utf-8')

    is_match = bcrypt.checkpw(password_bytes, stored_hash_bytes)

    return is_match

def create_access_token(student_id: int) -> str:
    now = datetime.datetime.now(datetime.UTC) 
    hour_from_now = datetime.timedelta(hours = 1)

    expiration = now.timestamp() + hour_from_now.timestamp()

    payload = {
        "student_id": student_id,
        "exp": expiration
    }

    token = jwt.encode(payload, THEE_KEY, algorithm="HS256")

    return token

def verify_access_token(token: str) -> int:
    try:

        decoded_payload = jwt.decode(
            token,
            THEE_KEY,
            algorithms=["HS256"]
        )

        return int(decoded_payload["student_id"])

    except jwt.ExpiredSignatureError as e:
        raise ValueError("Session expired. Please log in again.") from e
    except jwt.InvalidTokenError as e:
        raise InvalidTokenError("Malformed authentication token.") from e

