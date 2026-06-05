import sys
import os
import subprocess

builtins = ["exit", "echo", "type"]

def main():
    while True:
        sys.stdout.write("$ ")
        usr_input = input()
        command = usr_input.split(" ")[0]
        if usr_input == "exit":
            return
        elif command == "echo":
            print(" ".join(usr_input.split(" ")[1:]))
        elif command == "type":
            type(" ".join(usr_input.split(" ")[1:]))
        else:
            is_exec = check_if_exec(command)
            if is_exec:
                result = subprocess.run(
                    [command] + usr_input.split(" ")[1:], capture_output=True, text=True
                )
                print(result.stdout.strip() + result.stderr.strip())
            else:
                print(usr_input + ": command not found")

def check_if_exec(input):
    # Unix system
    if os.pathsep == ":":
        paths = os.environ["PATH"].split(":")
    # Windows system
    elif os.pathsep == ";":
        paths = os.environ["PATH"].split(";")
    else:
        print("Unknown system type")
        return
    for dir in paths:
        if not os.path.isdir(dir):
            continue

        try:
            for filename in os.listdir(dir):
                full_path = os.path.join(dir, filename)
                if os.path.isfile(full_path) and os.access(full_path, os.X_OK) and filename == input:
                    return full_path
        except PermissionError:
            pass   

    return False         

def type(input):
    if input in builtins:
        comm_type = "builtin"
        print(input + " is a shell " + comm_type)
    else:
        if os.pathsep == ":":
            # Unix system
            paths = os.environ["PATH"].split(":")
        elif os.pathsep == ";":
            # Windows system
            paths = os.environ["PATH"].split(";")
        else:
            print("Unknown system type")
            return
        
        for dir in paths:
            if not os.path.isdir(dir):
                continue

            try:
                for filename in os.listdir(dir):
                    full_path = os.path.join(dir, filename)
                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK) and filename == input:
                        print(input + " is " + full_path)
                        return
            except PermissionError:
                pass            

        print(input + ": not found")


if __name__ == "__main__":
    main()
