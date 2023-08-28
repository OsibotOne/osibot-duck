#
# osibot-duck
#
# Backup Upload Script
#
# Changes Required:
# 1. Record output "upload-backup successful" to vessel.log file
# 2. Record output "upload-backup error - {error msg}" to vessel.log file
# 3. Amend time&date to end of remotepath file for uploads


from paramiko import SSHClient, AutoAddPolicy
from datetime import datetime

# Configuration
HOST = "home235874866.1and1-data.host"
PORT = 22
USERNAME = "*********"
PASSWORD = "*********"


def file_transfer_server(host, port, username, password):
 
    try:
        # Open SSH
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())  # If not this line, it will create SSH exception
        ssh.connect(host, port, username, password)
        # Open an SFTP
        sftp = ssh.open_sftp()
        # Upload 
        sftp.put(localpath="/home/pi/backup/now/vessel.dat",
                 remotepath="/download/backup/vessel.dat")
        # Upload 
        sftp.put(localpath="/home/pi/backup/now/science.dat",
                 remotepath="/download/backup/science.dat")
        # Close connection
        sftp.close()
        ssh.close()
        
    except Exception as error:
        return f"{type(error).__name__}: {error}"

    else:
        return "uploaded successfully"


def main():
    what = "upload-backup"
    # Get time now
    now = datetime.now().strftime("%Y-%m-%d %H%M%S")
    # Upload and Download file
    message = file_transfer_server(HOST, PORT, USERNAME, PASSWORD)
    with open("./home/pi/data/comms.log", 'a') as file:       # open log.dat as append only
        file.write(f"{what}:{now}:{message}" + '\n')  # write saving message to the file

# The script can run individually or be part of other program.
if __name__ == "__main__":
    main()
