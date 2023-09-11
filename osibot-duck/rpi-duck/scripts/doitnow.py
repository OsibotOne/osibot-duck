# osibot-duck
# Python version 3.10
# Main Remote Command Script
import os
import subprocess
from datetime import datetime


# ------------------------------Read /home/pi/command/doit.now file---------------------------------------------------
def read_do_it(path):
    with open(path, "r") as file:
        # Read each line from the file
        args_list = []
        for line in file:
            # Split the line by commas to get individual values
            values = line.strip().split(',')
            # Ensure there are at least 2 values before passing them to the function
            if len(values) > 1 and values[0].isdigit():
                # Create a list to store arguments
                args = list(values)
                args_list.append(args)
            else:
                return "Error occurs: not enough values"
    return args_list


# --------------------------------Manual select script t execute---------------------------------------------------
def do_it_now_manual(CommandNumber, command_path):
    """
    This function execute the scripts according to the "doit.now" ask for.
    Below is the example of "doit.now" format.
    1,upload-backup.py
    2,goto-now.py,14.783687328434,-129.2323232737237
    3,relay-manual.py,6,1,0
    The function will execute the "upload-backup.py" if CommandNumber = 1.
    :param int CommandNumber: Select a command
    :param str command_path: A list of commands from a text file
    :return: stdout, stderr, error
    """
    try:
        command_list = read_do_it(command_path)
        select_command = [command_arg for command_arg in command_list if int(command_arg[0]) == CommandNumber][0]
        select_command.pop(0)
        command = ["python"] + select_command
        # Execute the script and pass arguments
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Wait for the process to finish and capture the output
        stdout, stderr = process.communicate()
        return stdout, stderr

    except Exception as error:
        return error


# --------------------------------------Auto Execute all commands (run scripts in order sequence)---------------------
def do_it_now_auto(command_path):
    """
    This function execute all scripts in the order of the "doit.now" provide.
    Below is the example of "doit.now" format.
    1,upload-backup.py
    2,goto-now.py,14.783687328434,-129.2323232737237
    3,relay-manual.py,6,1,0
    The function will execute all 3 scripts in sequence.
    :param str command_path: A list of commands from a text file
    :return: stdout, stderr, error
    """
    try:
        command_list = read_do_it(command_path)
        results = []
        for command_arg in command_list:
            command_arg.pop(0)
            command = ["python"] + command_arg
            # Execute the script and pass arguments
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Get return_code
            return_code = process.wait()
            # Wait for the process to finish and capture the output
            stdout, stderr = process.communicate()
            if return_code != 0:      # If there is error, stop the process
                results = results.append(stderr)
                return False, results
            else:
                results = results.append(stdout)

    except Exception as error:
        return False, error

    else:
        return True, results


def main():
    what = "doitnow.py"
    file_path = "./doit.now"
    # Get time now
    now = datetime.now().strftime("%Y-%m-%d %H%M%S")
    # ------------------------------------ if "doit.now" exist -----------------------------------------
    if os.path.exists(file_path):
        with open("/home/pi/now/result.now", "w") as file:  # "w" mode will overwrite the file if already present
            file.write(f"{what}:{now}:New Commands Received" + '\n')
        ## Execute command
        message = do_it_now_auto(file_path)
        # ------------------------------ if Executed Successful ---------------------------------------
        if message[0]:
            with open("/home/pi/now/result.now", "a") as file:      # Append result to result.now
                file.write(f"{what}:{now}:New Commands Executed Successfully" + '\n')
        # ------------------------------ if Executed Unsuccessful -------------------------------------
        else:
            with open("/home/pi/now/result.now", "a") as file:      # Append result to result.now
                file.write(f"{what}:{now}:New Commands Executed Unsuccessfully - {message[1]}" + '\n')
        # ----------------------------alwasy delele "doit.now" after executing ------------------------
        os.remove(file_path)
    # -----------------------------if "doit.now" not exist" -------------------------------------------          
    else:
        with open("/home/pi/now/result.now", "w") as file:
            file.write(f"{what}:{now}:No such file" + '\n')

    # ----------------------------- Reuslt will alwasy record to vessel.log ---------------------------
    # write result into vessel.log
    with open("/home/pi/now/result.now", "r") as file_result:  # Append result to result.now
        lines = file_result.read()
        with open("./home/pi/data/vessel.log", 'a') as file_vessel:  # vessel.log as append only
            file_vessel.write(lines)  # write saving message to the file
    
