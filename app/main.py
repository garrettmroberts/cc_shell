import sys
import os
import subprocess

builtins = ["exit", "echo", "type"]

def main():
    is_running = True
    while is_running:
        sys.stdout.write("$ ")
        usr_input = input()
        command = usr_input.split(" ")[0]
        if command in builtins:
            is_running = run_builtin(usr_input)
        else:
            is_exec = check_if_exec(command)
            if is_exec:
                result = subprocess.run(
                    [command] + usr_input.split(" ")[1:], capture_output=True, text=True
                )
                print(result.stdout.strip() + result.stderr.strip())
            else:
                print(usr_input + ": command not found")

def run_builtin(input):
    cmd = input.split(" ")[0]
    args = input.split(" ")[1:]
    if cmd == "exit":
        return False
    elif cmd == "echo":
        print(" ".join(args))
    elif cmd == "type":
        type(args[0])
    return True


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
        exec_path = check_if_exec(input)
        if exec_path:
            print(input + " is " + exec_path)
        else:
            print(input + ": not found")


if __name__ == "__main__":
    main()
