from Sensor import Sensor
from Setup import Setup
from time import sleep
from datetime import datetime

def main():
    # Create Setup object
    bus = Setup()

    # Create Sensor object
    sense = Sensor()

    # Setup the SPI bus
    bus.busSetup()

    while True:
        # Retrieve the SPI bus
        channel_1, channel_2 = bus.getBus()

        # Setup the sensors
        sense.setTemperatureInC(channel_1)

        sense.setTemperatureInF(channel_1)

        sense.setLuminosity(channel_2)

        # Fetch temperature in degrees C
        temperatureC = sense.getTemperatureInC()

        # Fetch temperature in degrees F
        temperatureF = sense.getTemperatureInF()

        # Fetch luminosity as a percentage
        luminosity = sense.getLuminosity()

        # Open file for output
        outfile = open(r"/home/pi/share/data.txt", "a")

        # Write temperature and luminosity readings to file
        outfile.write("\n{:5.2f}\t\t{:6.2f}\t\t{}".format(temperatureC,luminosity,datetime.now()))

        # Close file stream
        outfile.close() # Close the input file

        # time delay between readings
        sleep(30)

main() # call the main function
