# offzone.py
# By Hamish Dowell (www.hamishdowell.com)
# program defines timezones when light will be off

from __future__ import absolute_import, division, print_function, unicode_literals
from bh1750 import BH1750
import RPi.GPIO as GPIO
import time
import os

# Setting up GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)	# Board numbering scheme
GPIO.setup(15, GPIO.OUT)		# Pin 15 = Light Relay

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
	

override = open("/home/pi/lighting/override.status","r")
overrideMinutes = int(override.read())
override.close()
if overrideMinutes > 0:
   # We are in override, so decrement the counter
   override = open("/home/pi/lighting/override.status","w")
   override.write(str(overrideMinutes - 1))
   override.close()
else:

   lightstat = open("/home/pi/lighting/lights.status","r")
   lights = lightstat.read()
   lightstat.close()

   print("DEBUG: Lights are currently " + lights)

   if lights == "ON":
      # We are in the off zone and the lights are on, so switch them OFF
      print("Switching the lights OFF due to being outside hours.")
      lightstat = open("/home/pi/lighting/lights.status","w")
      lightstat.write("OFF")
      lightstat.close()
      GPIO.output(15, True)
