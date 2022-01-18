#
#           bh1750.py
# Read data from a BH1750 digital light sensor.
#
# Author : Matt Hawkins
# Date   : 26/06/2018
#
# For more information please visit :
# https://www.raspberrypi-spy.co.uk/?s=bh1750
#
#---------------------------------------------------------------->

import RPi.GPIO as GPIO
import smbus
import time
from datetime import datetime

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) #just for terminal purposes
GPIO.setup(15,GPIO.OUT)


# Define some constants from the datasheet

DEVICE     = 0x23 # Default device I2C address

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number. Optional parameter 'decimals'
  # will round to specified number of decimal places.
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=DEVICE):
  # Read data from I2C interface
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)

def setLightLevel():
  a = input("Enter the value: ")
  a = int(a)
  return a

def setTimeZones():
  time_zone = []
  temp1 = int(input("Enter number of ON zones: "))
  for i in range(temp1):
    time_zone.append(float(input("Enter starting hour of zone: ")))
    time_zone.append(float(input("Enter ending hour of zone: ")))
  return time_zone

def main():
  check = 0
  a=setLightLevel()
  print("a = ", a)
  time_zone=setTimeZones()
  number = int(len(time_zone)/2)
  while True:
    now = datetime.now()
    current_hour = int(now.strftime("%H"))

    for x in range(number):
      if (current_hour > time_zone[x*2] and current_hour < time_zone[x*2+1]):
        check = 1;
        break;
      else:
        check = 0;

    if check == 1:
      lightLevel=readLight()
      print("Light Level : " + format(lightLevel,'.2f') + " lx")
      if lightLevel<=a:
        GPIO.output(15,GPIO.LOW)
        print("Output off")
      else:
        GPIO.output(15,GPIO.HIGH)
        print("Output on")
    else:
      print("Now in OFF zone, waiting for ON zone to set the light!")
    
    time.sleep(2)

if __name__=="__main__":
   main()


