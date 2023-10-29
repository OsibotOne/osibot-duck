# Osibot-Duck
# Python 3.11.5

# Structure  param.sh  Param Name, Param Value
# Example   goto.sh js_gain, 0.5

# Connects to Autopilot via MAVLINK protocol (USB Serial)
# Disarms vehicle if armed
# Uploads new vehicle parameter from script arguments above
# Rearms vehicle if previously armed.

# Outputs success or any errors to vessel.log file

# https://mavlink.io/en/mavgen_python/
# https://github.com/ArduPilot/pymavlink
# https://www.ardusub.com/developers/pymavlink.html#armdisarm-the-vehicle

import re
import sys
from datetime import datetime

from pymavlink import mavutil

import mavcontrol as mv


def disarm_mav(master):
    """
        check arm status and disarm armed mav
        Args:
            master: device connection
        Returns:
            pre_arm_status: previous arm status
            msg_check_arm: disarm armed mav results
    """
    master.wait_heartbeat()
    # Disarms vehicle if armed
    pre_arm_status = mv.check_is_arm(master)
    if pre_arm_status == 1:
        # Change to manual mode and disarm
        msg_check_arm = mv.mode_change(master, "manual", "disarm")
        # If change not successful, return error message
        if mv.check_is_arm(master) == 0:
            msg_check_arm = False
    else:
        msg_check_arm = "The mav was disarmed"
    return pre_arm_status, msg_check_arm

def param_change(path, param, value):
    """
        Search and change a parameter value in a script
        Args:
            path: script path
            param: parameter to search
            value: value to change
        Returns:
            message: result of change
    """
    try:
        # Read the script
        with open(path, "r") as script_file:
            script_content = script_file.read()

        # Use regular expressions to find and replace the parameter value
        pattern = re.compile(fr'{param}\s*=.*\..*')
        script_content = pattern.sub(f'{param} = {value}', script_content)

        # Write the updated content back to the script
        with open(path, "w") as script_file:
            script_file.write(script_content)

    except Exception as error:
        return error

    else:
        return f"Parameter '{param}' updated to {value} in {path}"





def main():
    MAV_PORT = '******'
    # Create the connection
    master = mavutil.mavlink_connection(MAV_PORT)

    # Pre-check MAV
    pre_check = disarm_mav(master)  # Return a tuple  (pre_arm_status, msg_check_arm)
    # If status is disarmed
    if pre_check[1]:
        # ------------------------Param searching and value replacing---------------------------
        # Specify the path to the Python script
        script_path = sys.argv[1]
        # Define the parameter you want to search for and the new value
        search_param = sys.argv[2]
        new_value = sys.argv[3]
        # Perform parameter value change
        msg_param = param_change(script_path, search_param, new_value)

        # ----------------------------Rearms vehicle if previously armed----------------------
        if pre_check[0] == 1:
            msg_end = f"""{msg_param} and {mv.mode_change(master, "AUTO", "arm")}"""
        else:
            msg_end = f"""{msg_param} and {mv.mode_change(master, "AUTO", "disarm")}"""
    else:
        msg_end = "No action, unable to disarm before change parameters"

    # Combine messages
    message = f"pre_check: {pre_check[1]}, new_mission: {msg_end}"

    # Get time now
    now = datetime.now().strftime("%Y-%m-%d %H%M%S")

    # Save to vessel.log
    with open("./logs/vessel.log", 'a') as file:  # open as append only
        file.write(f"{now}:{message}" + '\n')  # write saving message to the file


if __name__ == "__main__":
    main()
