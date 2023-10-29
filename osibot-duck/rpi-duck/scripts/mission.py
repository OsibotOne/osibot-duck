# Osibot-Duck
# Python 3.11.5
import sys

# Structure  mission.sh  Mission.file
# Example   mission.sh mission101.dat
from datetime import datetime
from paramiko import SSHClient, AutoAddPolicy
from pymavlink import mavutil
import mavcontrol as mv


def file_transfer_server(host,
                         port,
                         username,
                         password,
                         local_file_path,    # Here is misson.file
                         remote_file_path    # location to upload
                         ):
    """
        Upload files
        Args:
            sftp host, port, username, password, file_path
        Returns:
            Exception: error message
            Completed: "uploaded successfully"
    """
    try:
        # Open SSH
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())  # If not this line, it will create SSH exception
        ssh.connect(host, port, username, password)
        # Open an SFTP
        sftp = ssh.open_sftp()
        # Upload files
        sftp.put(localpath=local_file_path,
                 remotepath=remote_file_path)
        # Close connection
        ssh.close()
        sftp.close()

    except Exception as error:
        return f"{type(error).__name__}: {error}"

    else:
        return "uploaded successfully"


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


# Uploads new vehicle mission from script arguments above
def new_mission(remote_file_path):
    """
        read new mission file
        Args:
            remote_file_path: mission file
        Returns:
            new_mission: mode
    """
    with open(remote_file_path, 'r') as data:
        new_mode = data.readlines()  # assume data structure is [mode, arm]
    return new_mode[0]

def main():
    # Upload Configuration
    HOST = "home235874866.1and1-data.host"
    PORT = 22
    USERNAME = "*******"
    PASSWORD = "*******"
    LOCAL_PATH = sys.argv[1]
    MAV_PORT = '******'

    # Upload file
    upload_msg = file_transfer_server(HOST, PORT, USERNAME, PASSWORD, LOCAL_PATH, "./mission.file")

    # Create the connection
    master = mavutil.mavlink_connection(MAV_PORT)

    # Pre-check MAV
    pre_check = disarm_mav(master)    # Return a tuple  (pre_arm_status, msg_check_arm)

    if pre_check:
        # New Mission Command
        new_mode = new_mission("mission.file")  # The remote path according to the setting
        # Sets vehicle mode to AUTO (?)
        # Rearms vehicle if previously armed.
        if pre_check[0]:
            msg_new_mission = mv.mode_change(master, new_mode, "arm")
        else:
            msg_new_mission = mv.mode_change(master, new_mode, "disarm")
    else:
        msg_new_mission = "No action, unable to disarm before assign new mission"
    # Combine messages
    message = f"pre_check: {pre_check[1]}, new_mission: {msg_new_mission}"

    # Get time now
    now = datetime.now().strftime("%Y-%m-%d %H%M%S")
    with open("./logs/vessel.log", 'a') as file:  # open as append only
        file.write(f"{now}:{message}" + '\n')  # write saving message to the file

if __name__ == "__main__":
    main()


# https://mavlink.io/en/mavgen_python/
# https://github.com/ArduPilot/pymavlink
# https://www.ardusub.com/developers/pymavlink.html#armdisarm-the-vehicle
