#
# osibot-duck
#
# Update Upload Script
#
# Changes Required:
# 1. Record output "upload-update successful" to vessel.log file
# 2. Record output "upload-update error - {error msg}" to vessel.log file


from paramiko import SSHClient, AutoAddPolicy
from datetime import datetime

# Configuration
HOST = "home235874866.1and1-data.host"
PORT = 22
USERNAME = "*********"
PASSWORD = "*********"


def file_transfer_server(host, port, username, password):
    """
           Upload "now.dat" and download "doit.now"
           Args:
               sftp host, port, username, password
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
        # Download "doit.now"
        sftp.get(remotepath="/download/doit.now",
                 localpath="/home/pi/command/doit.now")
        # Download "mission.now"
        sftp.get(remotepath="/download/mission.now",
                 localpath="/home/pi/command/mission.now")
        # Upload "now.dat"
        sftp.put(localpath="/home/pi/now/now.dat",
                 remotepath="/download/now/now.dat")
        # Upload "result.now"
        sftp.put(localpath="/home/pi/now/result.now",
                 remotepath="/download/now/result.dat")
        # Upload "cam1-web.jpg"
        sftp.put(localpath="/home/pi/pics/cam1-web.jpg",
                 remotepath="/download/now/cam1-web.jpg")
        # Close connection
        sftp.close()
        ssh.close()
        
    except Exception as error:
        return f"error - {type(error).__name__}: {error}"

    else:
        return "successful"


def main():
    what = "upload-update"
    # Get time now
    now = datetime.now().strftime("%Y-%m-%d %H%M%S")
    # Upload and Download file
    message = file_transfer_server(HOST, PORT, USERNAME, PASSWORD)
    with open("./home/pi/data/comms.log", 'a') as file:       # open log.dat as append only
        file.write(f"{what}:{now}:{message}" + '\n')  # write saving message to the file

# The script can run individually or be part of other program.
if __name__ == "__main__":
    main()
