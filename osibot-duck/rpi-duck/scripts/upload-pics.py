# Pics Upload Script
#
# Changes Required:
# 1. Record output "upload-pics successful" to vessel.log file
# 2. Record output "upload-pics error - {error msg}" to vessel.log file
# 3. Amend time&date to end of remotepath file for uploads


from paramiko import SSHClient, AutoAddPolicy
from datetime import datetime
import os

# Configuration
HOST = "home235874866.1and1-data.host"
PORT = 22
USERNAME = "*********"
PASSWORD = "*********"


def file_transfer_server(host, port, username, password, upload_time):
    try:
        # Open SSH
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())  # If not this line, it will create SSH exception
        ssh.connect(host, port, username, password)
        # Open an SFTP
        sftp = ssh.open_sftp()
        # Rename zip file
        os.rename("/home/pi/backup/now/cam1.zip",
                  f"/home/pi/backup/now/cam1_{upload_time}.zip")
        sftp.put(localpath=f"/home/pi/backup/now/cam1_{upload_time}.zip",
                 remotepath=f"/home/pi/backup/now/cam1_{upload_time}.zip")
        # Close connection
        sftp.close()
        ssh.close()

    except Exception as error:
        return f"error: {type(error).__name__}: {error}"

    else:
        return "successful"


def main():
    what = "upload-pics"
    # Get time now
    now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    f_date_time = datetime.now().strftime("%Y_%m_%d_%H_%M")  # date&time for filename
    # Upload and Download file
    message = file_transfer_server(HOST, PORT, USERNAME, PASSWORD, f_date_time)
    with open("./home/pi/log/vessel.log", 'a') as file:  # open log.dat as append only
        file.write(f"{what}:{now}:{message}" + '\n')  # write saving message to the file


# The script can run individually or be part of other program.
if __name__ == "__main__":
    main()
