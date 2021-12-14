#program defines timezones when light will be on

from __future__ import absolute_import, division, print_function, unicode_literals
from tsl2561 import TSL2561
import RPi.GPIO as GPIO
import time
import os

lowlux = 50

# Setting up the GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)	# Board numbering scheme
GPIO.setup(15, GPIO.OUT)	# Pin 15 = Light Relay


if not os.path.exists("/home/pi/lighting/lights.status"):
	print("DEBUG: lights.status file does not exist - creating it.")
	statusFile = open("/home/pi/lighting/lights.status","w")
	statusFile.write("ON")
	statusFile.close()

if not os.path.exists("/home/pi/lighting/override.status"):
	print("DEBUG: override.status file does not exist - creating it.")
	statusFile = open("/home/pi/lighting/override.status","w")
	statusFile.write("0")
	statusFile.close()
 
override = open("/home/pi/lighting/override.status","r+")
overrideMinutes = int(override.read())
if overrideMinutes > 0:
   # We are in override, so decrement the counter
   override.seek(0)
   override.write(str(overrideMinutes - 1))
   override.truncate
else:
   # We are not in override, so check the light level
   print("DEBUG: Lowlux = " + str(lowlux))

   # Get the current status of the lights
   lightstat = open("/home/pi/lighting/lights.status","r")
   lights = lightstat.read()
   lightstat.close()
   print("DEBUG: Lights are currently " + lights)

   tsl = TSL2561(debug=True)
   print("DEBUG: Lux value is currently " + str(tsl.lux()))

   if tsl.lux() < lowlux and lights == "OFF":
      # Light is low and lights are off, so switch them ON
      print("Switching the lights ON due to low light.")
      lightstat = open("/home/pi/lighting/lights.status","w")
      lightstat.write("ON")
      lightstat.close()
      GPIO.output(15, False)

   if tsl.lux() > lowlux and lights == "ON":
      # Light is good and lights are on, so switch them OFF
      print("Switching the lights OFF due to good light.")
      lightstat = open("/home/pi/lighting/lights.status","w")
      lightstat.write("OFF")
      lightstat.close()
      GPIO.output(15, True)

override.close()
