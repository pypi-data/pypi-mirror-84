from Sensor import Sensor
from Setup import Setup
from time import sleep

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

        # print output
        print("Temperature in degrees Celsius: {:5.2f} deg".format(temperatureC))

        print("Temperature in degrees Fahrenheit: {:5.2f} deg".format(temperatureF))

        print("Luminosity as a percentage: {:6.2f} %".format(luminosity))

        print("\n")

        # time delay between readings
        sleep(1)

main() # call the main function
