# lightserver.py
# By Hamish Dowell (www.hamishdowell.com)
# For more information, see https://www.makeuseof.com/?p=801553

# This script runs a basic web server that listens for override commands

# Load some libraries
import RPi.GPIO as GPIO
import time
from bottle import route, run, template
import os

# Set up the GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)	# Board numbering scheme
GPIO.setup(15, GPIO.OUT)	# Pin 15 = Light Relay
GPIO.output(15, True)  		# Switch lights off when we start the server (cron will switch them on when necessary)


# Check if the control files are in place
if not os.path.exists("/home/pi/lighting/lights.status"):
   statusFile = open("/home/pi/lighting/lights.status","w")
   statusFile.write("ON")
   statusFile.close()

if not os.path.exists("/home/pi/lighting/override.status"):
   statusFile = open("/home/pi/lighting/override.status","w")
   statusFile.write("0")
   statusFile.close()

# Set up a default index page
@route('/')
def index():
   return 'Nothing to see here. Bye.'

# Set up a status page
@route('/lightstatus')
def lightstatus():
   lightStat = open("/home/pi/lighting/lights.status","r")
   lights = lightStat.read();
   lightStat.close()
   return lights

# Set up the override ON page
@route('/overrideon/:minutes')
def overrideon(minutes=0):
   if minutes == '0':
      return 'No minute value specified.'
   
   overrideFile = open("/home/pi/lighting/override.status","w")
   overrideFile.write(minutes)
   overrideFile.close()

   statusFile = open("/home/pi/lighting/lights.status","w")
   statusFile.write("ON")
   statusFile.close()

   GPIO.output(15, False)  # Switch the lights on
 
   return 'Lights on for ' + minutes + ' minutes.'

# Set up the override OFF page
@route('/overrideoff')
def overrideoff():

   overrideFile = open("/home/pi/lighting/override.status","w")
   overrideFile.write("0")
   overrideFile.close()

   statusFile = open("/home/pi/lighting/lights.status","w")
   statusFile.write("OFF")
   statusFile.close()

   GPIO.output(15, True)
 
   return 'Lights off'

@route('/getoverrideremaining')
def getoverrideremaining():
   overrideFile = open("/home/pi/lighting/override.status","r")
   timeleft = overrideFile.read()
   overrideFile.close()
   return timeleft

# Run the webserver
run(host='0.0.0.0', port=1234)
