import docker
from docker.errors import NotFound, APIError
import tarfile
import io
import threading
from expected_outputs import problems


class SandboxExecutionTimeout(Exception):
    #Raised when the user's code runs past its allowed time limit
    pass

#connect to the local docker daemon
client = docker.from_env()


def run_code(code_to_run: str):

    local_container = client.containers.run(
        "python:3.13.5",
        mem_limit="256m",
        command=["tail", "-f", "/dev/null"],
        nano_cpus=int(5e8),
        detach=True,
        network_disabled=True
        
    )
    local_bytes = code_to_run.encode("utf-8")#Turns into bytes
    watchdog = None
    max_execution_time = 5.0

    #Used the same error exception as in the finally statment due possibility that the kill() statement acts first/ Race Condition
    def timeout_handler():
        try:
            print("Timeout triggered. Killing container.")
            local_container.kill()
        except NotFound as e:
            print(f"Error: The requested resources was not found. Details: {e.explanation}")
        except APIError as e:
            print(f"A different docker API error occured: {e}")   
         
         
    local_tar_stream = io.BytesIO()
    try:
        with tarfile.open(fileobj= local_tar_stream, mode='w') as local_tar:

            tar_info = tarfile.TarInfo(name = "user_submission.txt")
            # Write the bytes into the tar_archive
            tar_info.size = len(local_bytes)# The size of the local tar file for the given submission
            local_tar.addfile(tar_info, io.BytesIO(local_bytes))

            # Starts from the beginning of the stream 
        local_tar_stream.seek(0)
        local_container.put_archive("/tmp", local_tar_stream)


        watchdog = threading.Timer(max_execution_time, timeout_handler )
        watchdog.start()

        print("Executing code inside sandbox...")
        result = local_container.exec_run(["python" , "/tmp/user_submission.txt"])


        local_container_info = client.api.inspect_container(local_container.id)
        if not local_container_info['State']['Running'] and local_container_info['State']['ExitCode'] == 137:
           
            raise SandboxExecutionTimeout("Execution exceeded the allowed time limit")

        return result
    
    finally:
        if watchdog is not None:
            watchdog.cancel()
        #prevents the buildup of containers
        try:
            local_container.remove(force=True)
            print("container was successfully removed.")
        except NotFound as e:
            print(f"Error: The requested resources was not found. Details: {e.explanation}")
        except APIError as e:
            print(f"A different docker API error occured: {e}")

 #Creates multilined structure
multi_line = []
current_difficulty = None
striped_user_input = None
submit_typed = "Submit"

while True:
    user_input = input("Select Problem(easy, medium, or hard (when finished type 'Submit')): ")
    striped_user_input = user_input.strip().lower()

    if striped_user_input in problems:

        if striped_user_input != current_difficulty:

            multi_line.clear()
        current_difficulty = striped_user_input

        print(problems[current_difficulty]["description"])
        continue

    if striped_user_input == submit_typed.lower():
        if not current_difficulty:
            print("Error: You must select a problem before submitting.")
            continue
        if not multi_line:
            print("Error: You cannot submit empty code! Please write your solution.")
            continue
        break

    if not current_difficulty:
        print("Error: Please select a difficulty('easy', 'medium', or 'hard')")
        continue
    
    multi_line.append(user_input)

final_statement = "\n".join(multi_line)
print(f"final submission: {final_statement} ")


try:
    result = run_code(final_statement)
    if result.exit_code != 0:
        print(f"Runtime error:{result.exit_code}")    
    else:
        print(result.exit_code)
        decoded_result = result.output.decode("utf-8")

        print(decoded_result)
        # Compares the result to the expected output
        if(decoded_result.strip() == problems[current_difficulty]["expected"]):
            print("correct")
        else:
            print("incorrect")

except SandboxExecutionTimeout as e:
    print("Execution Failed")
    print(e)
