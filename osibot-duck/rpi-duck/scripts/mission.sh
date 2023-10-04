# Osibot-Duck

# Structure  mission.sh  Mission.file
# Example   mission.sh mission101.dat

# Connects to Autopilot via MAVLINK protocol (USB Serial)
# Disarms vehicle if armed
# Uploads new vehicle mission from script arguments above
# Sets vehicle mode to AUTO
# Rearms vehicle if previously armed.

# Outputs success or any errors to vessel.log file

# https://mavlink.io/en/mavgen_python/
# https://github.com/ArduPilot/pymavlink
# https://www.ardusub.com/developers/pymavlink.html#armdisarm-the-vehicle

