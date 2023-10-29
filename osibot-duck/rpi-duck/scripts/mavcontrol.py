# Osibot-Duck
# Python 3.11.5

# Structure  mavcontrol.sh  Mode, Arm
# Example   mavcontrol.sh auto, arm
# Example2  mavcontrol.sh manual, disarm

import sys
import time
from datetime import datetime
from pymavlink import mavutil


def check_is_arm(master):
    """
    Check if the mav is armed or not
    """
    msg = master.recv_match(type='HEARTBEAT', blocking=True)
    # Return True if armed else False
    if bool(msg.base_mode > 66):
        return 1
    else:
        return 0


def check_is_mode_change(master):
    """
        Check if the mode has been changed accordingly
    """
    msg = master.recv_match(type='HEARTBEAT', blocking=True)
    # Return True if armed else False
    return msg.custom_mode


def mode_change(master, mode, arm):
    """
    This function can change the mode of the bot
    Args:
        str port: connection port setting
        str mode: AUTO, manual, .....
        str arm: arm or disarm
    return:
        str -> a message of results
    """
    try:
        # Wait a heartbeat before sending commands
        master.wait_heartbeat()
        ## =======================Mode Setting===========================
        mode = mode.upper()  # Change to upper letter as requires

        # Check if mode is available
        if mode not in master.mode_mapping():
            mode_msg = 'Unknown mode : {}'.format(mode)
            print('Try:', list(master.mode_mapping().keys()))
            sys.exit(1)
        # Get mode ID
        mode_id = master.mode_mapping()[mode]
        # Set new mode
        master.mav.set_mode_send(
            master.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode_id)

        # Check if mode has been changed
        retry = 0
        if check_is_mode_change(master) == mode_id:
            mode_msg = f"Mode has been changed to {mode}"
        else:
            while not check_is_mode_change(master) == mode_id and retry < 3:  # If check_is_arm(master) != True
                time.sleep(30)
                retry += 1
                master.mav.set_mode_send(
                    master.target_system,
                    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                    mode_id)
            if retry < 3:
                mode_msg = f"Mode has been changed to {mode}, retry: {retry}"
            else:
                mode_msg = "Fail to change mode"

        ## ========================Arm or Disarm==========================
        # Presetting
        if arm.lower() == "arm":
            is_arm = 1  # arm
        elif arm.lower() == "disarm":
            is_arm = 0  # disarm
        else:
            return "unknown command"

        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            is_arm,  # 1 as arm, 0 as disarm
            0, 0, 0, 0, 0, 0)

        # Arming
        if is_arm == 1:
            master.motors_armed_wait()
            retry = 0
            # retry 3 times and wait 30 second each times
            time.sleep(3)
            while check_is_arm(master) == 0 and retry < 3:  # If check_is_arm(master) != True
                time.sleep(30)
                retry += 1
                master.motors_armed_wait()
            if check_is_arm(master):
                print('Armed!')
                return f"Armed, retry: {retry}"
            else:
                return "Fail to arm"

        # Disarming
        elif is_arm == 0:
            # wait until arming confirmed
            master.motors_disarmed_wait()
            retry = 0
            while check_is_arm(master) == 1 and retry < 3:  # If check_is_arm(master) != False
                time.sleep(30)
                retry += 1
                master.motors_disarmed_wait()
            if check_is_arm(master) == 0:  # If check_is_arm(master) != False
                print('Disarm!')
                return f"Disarm!: retry: {retry}"
            else:
                return "Fail to disarm"

    except Exception as error:
        return error


def main():
    # mode_change(sys.argv[1], sys.argv[2])
    PORT = '????????'
    # Create the connection
    master = mavutil.mavlink_connection(PORT)
    MODE = sys.argv[1]
    ARM = sys.argv[2]
    # Get time now
    now = datetime.now().strftime("%Y-%m-%d %H%M%S")
    # Get change massage
    message = mode_change(master, MODE, ARM)
    with open("./logs/vessel.log", 'a') as file:  # open as append only
        file.write(f"{now}:{message}" + '\n')  # write saving message to the file


# The script can run individually or be part of other program.
if __name__ == "__main__":
    main()
