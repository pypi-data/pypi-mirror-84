# Sensor class
class Sensor:
    def __init__(self,temperatureC=0,temperatureF=0,luminosity=0):
        self.__temperatureC = temperatureC
        self.__temperatureF = temperatureF
        self.__luminosity = luminosity

    def setTemperatureInC(self, channel=0):
        # calculate temperature in degrees C
        self.__temperatureC = channel/1024

    def setTemperatureInF(self, channel=0):
        # calculate temperature in degrees F
        self.__temperatureF = ((channel/1024)*(9/5))+32

    def setLuminosity(self, channel=0):
        # calculate luminosity as a percentage
        self.__luminosity = (channel-1850)/655

    def getTemperatureInC(self):
        # return temperature in C
        return self.__temperatureC

    def getTemperatureInF(self):
        # return temperature in F
        return self.__temperatureF

    def getLuminosity(self):
        # return luminosity as a percentage
        return self.__luminosity
