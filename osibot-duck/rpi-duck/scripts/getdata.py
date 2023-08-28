#
# osibot-duck
#
# Get Data Script
#
# Record all data in now.dat (Overwrite file), then amend data to vessel.dat
#
# Changes Required:



import time
from datetime import datetime


def collect_sensor_data():
    """
       Collect data from sensors
    """
    pass


def read_data(raw_data):
    """
        Reading unformat raw data and return cleaned data
        Args:
            raw_data: raw data from the sensor or files, can be a path
        Returns:
            Status: True or False
            Result: If True clean_data else error
     """
    clean_data = []                     # This can change according to the data format
    try:
        with open(raw_data, 'r') as now_dat:
            data = now_dat.readlines()  # do any transformation accordingly
            clean_data.append(data)
            
    except Exception as error:          # If encounter an error, record as error, except all errors for now
        return False, error

    else:
        return True, clean_data


def save_data(clean_data):
    """
        Saving clean data to vessel.dat
        Args:
            clean_data: new data for saving
        Returns:
            error or completed message
     """
    try:
        with open("./home/pi/data/vessel.dat", 'a') as file:  # open vessel.dat as append only
            for line in clean_data:
                file.write(line + '\n')        # write data into vessel.dat in right format
                
    except Exception as error:                 # If encounter an error, record as error, except all errors for now.
        return error

    else:
        return "script completed successfully"


# --------------------------------main script--------------------------------------
def main():
    # Get time now
    now = datetime.now().strftime("%Y-%m-%d %H%M%S")  
    
    # Try to collect new data
    is_read, result = read_data("./home/pi/now/now.dat")
    
    # If collect successfully
    if is_read:
        # Save new data to main data file, record the result
        status = save_data(result)
        with open("./home/pi/log/vessel.log", 'a') as file:      # open log.dat as append only
            file.write(f"getdata.py:{now}:{status}" + '\n')  # write saving message to the file
            
    # If collect failed       
    else:
        with open("./home/pi/log/vessel.log", 'a') as file:      # open log.dat as append only
            file.write(f"getdata.py{now}:{result}" + '\n')  # write saving message to the file


# The script can run individually or be part of other program.
if __name__ == "__main__":
    main()
