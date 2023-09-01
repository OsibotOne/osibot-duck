#
# osibot-duck
#
# Get Pic Script
#
# Changes Required:
# Output of Script should goto vessel.log file


import subprocess
import shutil
from datetime import datetime

# Get time now
now = datetime.now().strftime("%H%M_%Y%m%d")

# Run Bash commend save image to /img path
command = f"fswebcam -r 1920x1080 --no-banner /home/pi/now/cam1-web.jpeg"

# Return the Result of bash line
result = subprocess.run(command,
                        shell=True,
                        stdout=subprocess.PIPE,  # Capture standard output of the command
                        stderr=subprocess.PIPE,  # Capture standard error of the command
                        text=True  # Decode the output as text
                        )
# Get result message
if result.returncode == 0:
    shutil.copy("/img/cam1-web.jpeg", f"/img/cam1-{now}.jpeg")
    message = f"Cam1 Image Saved Successfully"
else:
    message = f"There is an error:{result.stderr}"
  
# Saveing message
with open("./home/pi/data/vessel.log", 'a') as file:  # open vessel.log as append only
    file.write(f"getpic.py::{now}:{message}" + '\n')  # write saving message to the file
