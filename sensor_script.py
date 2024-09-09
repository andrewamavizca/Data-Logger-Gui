import time
import random


"""
Here is where you will add the code to get the sensor data. you dont have to loop it here
the looping will happen in the if__name__ == "__main__": block below

This script is not ran by itself, it is ran by the gui.py script.

$: python gui.py

the gui.py script will run this script inside itself and capture the output to display in the gui.

You can also just run this script by itself to see the output in the terminal by running it directly. 

$: python sensor_script.py

"""

def wind_data():
    speed = random.uniform(0, 20)  # Simulate wind speed
    direction = random.choice(['N', 'S', 'E', 'W'])  # Simulate wind direction
    return speed, direction

def gps_data():
    lat = random.uniform(-90, 90)  # Simulate latitude
    lon = random.uniform(-180, 180)  # Simulate longitude
    return lat, lon

def methane_data():
    ch4_ppm = random.uniform(1.5, 2.5)  # Simulate methane data
    return ch4_ppm



if __name__ == "__main__":
    # Header for the table with fixed-width columns
    print(f'{"LAT":<14}{"LON":<14}{"U_wind":<12}{"U_dir":<8}{"CH4 ppm":<5}')
    print('-' * (14 + 14 + 12 + 8 + 7))  # Separator line

    while True:
        # Simulate fetching sensor data and printing it in fixed-width columns
        lat, lon = gps_data()
        wind_speed, wind_direction = wind_data()
        ch4 = methane_data()

        # Fixed-width columns for proper alignment
        print(f'{lat:<14.4f}{lon:<14.4f}{wind_speed:<12.2f}{wind_direction:<8}{ch4:<5.2f}')
        

        

        # set sleep to the slowest sensor data rate
        time.sleep(2)  
