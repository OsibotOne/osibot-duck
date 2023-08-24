import time


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
            clean_data: data that readable
     """
    clean_data = []                          # This can change according to the data format
    with open(raw_data, 'r') as now_dat:
        data = now_dat.readlines()           # do any transformation accordingly
    return clean_data


def save_data(clean_data):
    """
        Saving clean data to data.dat
        Args:
            clean_data: new data for saving
        Returns:
            None
     """
    with open("./data.dat", 'a') as file:    # open data.dat as append only
        for line in clean_data:
            file.write(line + '\n')          # write data in to data.dat in right format


# A loop for collecting data every 10 minutes
def main():
    is_on = True                             # Connect to Switch module for on and off
    while is_on:
        # Collect new data
        new_data = read_data("./now.dat")
        # Save new data to main data file
        save_data(new_data)
        # Delay for 10 minutes
        time.sleep(600)  # 600 seconds


# The script can run individually or be part of other program.
if __name__ == "__main__":
    main()
