## API Overview

The API contains the following files:
- **Setup.py** - creates the ADC (MCP3008) channel object
- **Sensor.py** - handles the sensor package's activities, qualities, and functionality

The following files illustrate the functioning of the API:
- application_console.py - prints the sensor output to the screen
- application_file.py - prints the sensor output to a text file (data.txt)

The API's functionality is interfaced with the Flask Web Application using **Samba file sharing**.

The API requires the following libraries to run:
- busio
- digitalio
- board
- adafruit_mcp3xxx.mcp3008
- adafruit_mcp3xxx.analog_in

These libraries can be installed on the Raspberry Pi using the following command:
- pip3 install adafruit-circuitpython-mcp3xxx
