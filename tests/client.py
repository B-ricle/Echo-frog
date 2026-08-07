import requests
import uuid 
from typing import Final

SEND_USER_ID: Final = True
 
#Create user the users message

user_id = str(uuid.uuid4())
solution_code= """
while True: pass
class Solution:
    def search(self, nums: list[int], target: int) -> int:
        left = 1
        right = len(nums) -1 

        while left <= right:
            mid = left + (right - left ) // 2

            if nums[mid] == target:
                return mid

            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid - 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1
            
            

the_solution = Solution()
the_array= the_solution.search([4, 5, 6, 7, 0, 1, 2], 0)
print(the_array)
"""
 
 #preparing the data/json's body 

payload = {
    "user_id": "test123",
    "code": solution_code,
    "problem_id": "hard"
}


if SEND_USER_ID:
    payload["user_id"] = str(uuid.uuid4())

try:
    #making the request to the backend server or app.py url
    response = requests.post("http://127.0.0.1:8000/submit", json = payload, timeout = 10)
    print(f"Actual Status: {response.status_code}")


    if response.status_code == 200:
        #Examining the response to ensure an error isnt there
        print(f"Status: {response.status_code}")
       
        #storing the response data 
        data = response.json()
        print(response.json())
        #Ensures that the key exists rather than trusting blindly that the key does exist

        try:    
            output = data['output']
            correct = data['correct']
            exit_code= data['exit_code']
            print(f"Server received : {output, correct, exit_code}")
        except KeyError as e:
            print("Server sent an unexpected response shape: ", e)

    elif response.status_code == 404:
        print("route not found") #The route to the backend isnt found
    
    elif response.status_code == 403:
        print("route exists but is forbidden") #The route to the backend exists though its forbidden

    elif response.status_code == 401:
        print("User missing identification")

except requests.exceptions.ConnectionError as error:
    print(f'Error : Cannot connect to server - {error}')#Connection error

except requests.exceptions.Timeout:
    print("Error: Request timed out")#Timed out of the server

except requests.exceptions.RequestException as error:
    print(f"Request failed: {error}")#this will show any other accounted for error



