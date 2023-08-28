#
# osibot-duck
#
# Update Upload Script
#
# Connect to AWS-Server via SFTP
# Check if doit.now file exists on server
# Download doit.now file. /download/doit.now
# Upload now.dat to server /upload/now.dat
# Upload cam1-temp.jpeg to server /upload/pics/cam1-temp.jpeg
# Report all errors to logfile

#Test SFTP Server to test with:

#username: acc764515107
#password: Nemo2023!
#server: home235874866.1and1-data.host
#port: 22
#protocol: SFTP

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
        sftp.get(remotepath="/upload/doit.now",
                 localpath="/home/pi/data/doit.now")
        # Upload "now.dat"
        sftp.put(localpath="/home/pi/data/now.dat",
                 remotepath="/download/data/now.dat")
        # Upload "cam1-web.jpg"
        sftp.put(localpath="/home/pi/pics/cam1-web.jpg",
                 remotepath="/download/now/cam1-web.jpg")
        # Close connection
        sftp.close()
        ssh.close()
        
    except Exception as error:
        return f"{type(error).__name__}: {error}"

    else:
        return "uploaded successfully"


def main():
    # Get time now
    now = datetime.now().strftime("%Y-%m-%d %H%M%S")
    # Upload and Download file
    message = file_transfer_server(HOST, PORT, USERNAME, PASSWORD)
    with open("./home/pi/data/log.dat", 'a') as file:       # open log.dat as append only
        file.write(f"{now}:{message}" + '\n')  # write saving message to the file

# The script can run individually or be part of other program.
if __name__ == "__main__":
    main()
