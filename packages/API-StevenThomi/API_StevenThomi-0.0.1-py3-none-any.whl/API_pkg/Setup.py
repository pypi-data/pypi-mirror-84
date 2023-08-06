####################################################################################
# The use of ADC (MCP3008) support libraries is credited to:
# https://github.com /adafruit/Adafruit_CircuitPython_MCP3xxx/blob/master/README.rst
####################################################################################

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class Setup:
    def __init__(self):
        self.__analogIn1 = 0
        self.__analogIn2 = 0

    def busSetup(self):
        # Setting up the ADC SPI interface
        # create the spi bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # create the cs (chip select)
        cs1 = digitalio.DigitalInOut(board.D5)
        cs2 = digitalio.DigitalInOut(board.D2)

        # create the mcp objects
        mcp1 = MCP.MCP3008(spi, cs1)
        mcp2 = MCP.MCP3008(spi, cs2)

        # retrieve analog input channel on pin 0, and pin 1
        analogIn1 = AnalogIn(mcp1, MCP.P0)
        analogIn2 = AnalogIn(mcp2, MCP.P1)

        # return analog input
        self.__analogIn1 = analogIn1
        self.__analogIn2 = analogIn2

    def getBus(self):
        # retrieve channel values
        analogIn1 = self.__analogIn1
        analogIn2 = self.__analogIn2

        # return channel values
        return analogIn1.value, analogIn2.value
