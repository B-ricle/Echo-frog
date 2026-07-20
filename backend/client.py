import requests
from models import ChatResponse
from pydantic import ValidationError
import uuid
from typing import Final

SEND_USER_ID: Final = True
 
#Create user the users message
user_message = input("Enter message: ")

user_id = str(uuid.uuid4())

 
 #preparing the data/json's body 

payload = {
    "message" : user_message
}

if SEND_USER_ID:
    payload["user_id"] = str(uuid.uuid4())

try:
    #making the request to the backend server or app.py url
    response = requests.post("http://127.0.0.1:8000/chat", json = payload, timeout = 10)
    print(f"Actual Status: {response.status_code}")


    if response.status_code == 200:
        #Examining the response to ensure an error isnt there
        print(f"Status: {response.status_code}")
       
        #storing the response data 
        data = response.json()
        print(response.json())
        #Ensures that the key exists rather than trusting blindly that the key does exist

        try:    
            reply = ChatResponse.model_validate(data)
            print(f"Server received : {reply}")
        except ValidationError as e:
            print("Server sent an unexpected response shape: ", e)

    elif response.status_code == 404:
        print("route not found") #The route to the backend isnt found
    
    elif response.status_code == 403:
        print("route exists but is forbidden") #The route to the backend exists though its forbidden

    elif response.status_code == 401:
        print("User missing identification")

except requests.exceptions.ConnectionError as error:
    print(f'Error : Cannot connect to server')#Connection error

except requests.exceptions.Timeout:
    print("Error: Request timed out")#Timed out of the server

except requests.exceptions.RequestException as error:
    print(f"Request failed: {error}")#this will show any other accounted for error



