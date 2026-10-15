import os
import sys
import subprocess
import pathlib

pipe_file = ""

def get_username():
    """
    Get the username of the current user.
    :return: the username of the current user
    """
    return os.getlogin()

def my_print(message, is_piped = False):
    """
    Print a message to the console or write it to a pipe file.
    :param message: the message to print
    :param is_piped: whether to write the message to the pipe file
    :return: None
    """
    if not is_piped:
        print(message)
    else:
        with open(pipe_file, "w") as f:
            f.write(message)

def run_external(command, redirection_file = None, is_piped = False):
    """
    Run an external command using subprocess.
    :param command: the command to run
    :param redirection_file: the file to redirect output to
    :param is_piped: whether the output is being piped
    :return: the result of the command execution
    """
    result = ""
    try:
        result = subprocess.check_output(command, text=True,stderr=subprocess.STDOUT)
        if redirection_file:
            # output contains unnecessary 1st line when redirected to a file
            result_lines = result.splitlines()
            with open(redirection_file, "w") as f:
                f.write("\n".join(result_lines[2:]))
        else:
            my_print(result, is_piped)
    except Exception as e:
        my_print(f"Error: {e}", is_piped)
    return result

def find_redirection(cmd_list):
    """
    Find the redirection operator in the command list.
    :param cmd_list: the list of command tokens
    :return: a tuple containing the command list without the redirection part and the redirection file if found
    """
    ll = len(cmd_list)
    for i, token in enumerate(cmd_list):
        if token == ">" and i + 1 < ll:
            return cmd_list[:i], cmd_list[i + 1]
    return cmd_list, None


def handle_command(command, is_piped = False):
    """
    Handle a shell command.
    :param command: the command to handle
    :param is_piped: whether the output is being piped
    :return: None
    """
    global current_path
    if command == "hello":
        my_print(f"Hello, {get_username()}!", is_piped)
        return
    cmd_list = command.split()
    if not cmd_list:
        return
    current_cmd = cmd_list[0]
    cmd_list, redirection_file = find_redirection(cmd_list)
    if current_cmd == "cd":
        try:
            if len(cmd_list) > 1:
                target = cmd_list[1]
                if target == "..":
                    target = os.path.dirname(current_path)
                if target == "/":
                    drive = pathlib.Path(os.getcwd()).parts[0]
                    target = drive + "\\"
                os.chdir(target)
            current_path = os.getcwd()
        except Exception as e:
            my_print(f"Error: {e}", is_piped)
        return
    if current_cmd == "ls":
        command_string = initial_path + "\\ls.bat"
        if len(cmd_list) > 1:
            command_string += " " + " ".join(cmd_list[1:])
        run_external(command_string, redirection_file, is_piped)
        return
    if current_cmd == "hexdump":
        command_string = initial_path + "\\hexdump.bat"
        if len(cmd_list) == 1:
            # no file is provided
            # pipe mode
            command_string += " " + pipe_file
        elif len(cmd_list) > 1:
            command_string += " " + " ".join(cmd_list[1:])
        run_external(command_string, redirection_file, is_piped)
        return
    if current_cmd == "grep":
        command_string = initial_path + "\\grep.bat"
        if len(cmd_list) == 2:
            # only pattern is provided, no file
            # pipe mode
            command_string += " " + pipe_file + " " + cmd_list[1]
        elif len(cmd_list) > 2:
            command_string += " " + " ".join(cmd_list[1:])
        run_external(command_string, redirection_file, is_piped)
        return
    if current_cmd == "help" or current_cmd == "?":
        my_print("Available commands:", is_piped)
        my_print("  hello      - Greet the user", is_piped)
        my_print("  cd <path>  - Change the current directory", is_piped)
        my_print("  ls <path>  - List files in the given directory", is_piped)
        my_print("  hexdump <file> - Display the hexadecimal content of a file", is_piped)
        my_print("  grep <file> <pattern> - Search for a pattern in the given file", is_piped)
        my_print("  exit       - Exit the shell", is_piped)
        return




initial_path = os.getcwd()
current_path = initial_path
pipe_file = initial_path + "\\___pipe___.txt"
while True:
    if os.path.exists(pipe_file):
        os.remove(pipe_file)
    command = input(f"{current_path}>>> ")
    command = command.strip().lower()
    if command == "exit":
        break
    command_list = command.split('|')
    command_list_len = len(command_list)
    for i, cmd in enumerate(command_list):
        handle_command(cmd, i<command_list_len-1)
