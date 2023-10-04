# Osibot-Duck

# Structure  mavcontrol.sh  Mode, Arm
# Example   mavcontrol.sh auto, arm
# Example2  mavcontrol.sh manual, disarm

# Connects to Autopilot via MAVLINK protocol (USB Serial)
# Changes vehicle mode
# Changes vehicle arm status
# Confirm change was successfull before proceeding, if failed retry 3 times after 30 seconds.

# Outputs success or any errors to vessel.log file

# https://mavlink.io/en/mavgen_python/
# https://github.com/ArduPilot/pymavlink
# https://www.ardusub.com/developers/pymavlink.html#armdisarm-the-vehicle

