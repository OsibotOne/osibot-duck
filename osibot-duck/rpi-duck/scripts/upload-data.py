#
# osibot-duck
#
# Data Upload Script
#
# Changes Required:
# 1. Record output "upload-data successful" to vessel.log file
# 2. Record output "upload-data error - {error msg}" to vessel.log file
# 3. Amend time&date to end of remotepath file for uploads

from paramiko import SSHClient, AutoAddPolicy
from datetime import datetime
import shutil

# Configuration
HOST = "home235874866.1and1-data.host"
PORT = 22
USERNAME = "*********"
PASSWORD = "*********"


def file_transfer_server(host, port, username, password, upload_time):
    """
           Upload "now.dat" and download "doit.now"
           Args:
               sftp host, port, username, password, upload_time)
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
        
        # File paths
        home_path = "/home/pi"
        server_path = "/download"
        
        # File names
        local_files = ["/data/vessel.dat",
                       "/data/science.dat",
                       "/log/vessel.log",
                       "/log/comms.log"]
        
        # Rename files
        files_to_upload = [f"/data/vessel_{upload_time}.dat",
                           f"/data/science_{upload_time}.dat",
                           f"/log/vessel_{upload_time}.log",
                           f"/log/comms_{upload_time}.log"]
        
        # Copy files, add date and time to the end of file name, and upload to the server
        for i in range(len(local_files)):
            shutil.copy(f"{home_path}{local_files[i]}", 
                        f"{home_path}{files_to_upload[i]}")
            sftp.put(localpath=f"{home_path}{files_to_upload[i]}",
                     remotepath=f"{server_path}{files_to_upload[i]}")
            
        # Close connection
        sftp.close()
        ssh.close()

    except Exception as error:
        return f"error - {type(error).__name__}:{error}"

    else:
        return "successful"


def main():
    what = "upload-data"
    # Get time now
    now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    f_date_time = datetime.now().strftime("%Y_%m_%d_%H_%M")  # date&time for filename

    # Upload and Download file
    message = file_transfer_server(HOST, PORT, USERNAME, PASSWORD, f_date_time)
    with open("./home/pi/data/vessel.log", 'a') as file:  # open log.dat as append only
        file.write(f"{what}:{now}:{message}" + '\n')  # write saving message to the file


# The script can run individually or be part of other program.
if __name__ == "__main__":
    main()
