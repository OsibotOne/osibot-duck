import subprocess
import shutil
from datetime import datetime

# Get time now
now = datetime.now().strftime("%H%M_%Y%m%d")

# Run Bash commend save image to /img path
command = f"fswebcam -r 1920x1080 --no-banner /img/cam1-temp.jpeg"

# Return the Result of bash line
result = subprocess.run(command,
                        shell=True,
                        stdout=subprocess.PIPE,  # Capture standard output of the command
                        stderr=subprocess.PIPE,  # Capture standard error of the command
                        text=True  # Decode the output as text
                        )

if result.returncode == 0:
    print("Image captured")
    shutil.copy("/img/cam1-temp.jpeg", f"/img/cam1-{now}.jpeg")
    print("Image saved")
else:
    print(f"There is an error:{result.stderr}")
