import docker

#connect to the local docker daemon
client = docker.from_env()

container = client.containers.run(
    "python:3.13.5",
    stdin_open=True, #keeps the STDIN open so that it is ready to recieve the user's input via string
    command="python -", #This allows the input to be read
    detach= True )

#Socket needs to gather live data so it leave stream as true so that the TCP/Unix domain socket can handle and deliver
socket = container.attach_socket(params={"stdin": True, "stream": True })
print(dir(socket))

users_code = "print('Hello from the Sandbox! ')"
#Turns the string into a bytes
socket.send(users_code.encode("utf-8"))

#closed socket meaning no more input
socket.close()
try:
    container.wait(timeout=10)
except Exception as e:
    print(f"Wait failed or timed out: {e} ")

#prints the output of the bytes of the input into a string 
output = container.logs().decode("utf-8")

print(output)
#prevents build up of containers
container.remove(force=True)




