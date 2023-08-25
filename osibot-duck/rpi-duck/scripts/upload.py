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
        sftp.get(remotepath="/command/doit.now",
                 localpath="doit.now")
        # Upload "now.dat"
        sftp.put(localpath="now.dat",
                 remotepath="/data/now.dat")
        # Close connection
        ssh.close()
        sftp.close()

    except Exception as error:
        return f"{type(error).__name__}: {error}"

    else:
        return "uploaded successfully"


def main():
    # Get time now
    now = datetime.now().strftime("%Y-%m-%d %H%M%S")
    # Upload and Download file
    message = file_transfer_server(HOST, PORT, USERNAME, PASSWORD)
    with open("./log.dat", 'a') as file:       # open log.dat as append only
        file.write(f"{now}:{message}" + '\n')  # write saving message to the file

# The script can run individually or be part of other program.
if __name__ == "__main__":
    main()
