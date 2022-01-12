#!/usr/bin/env python

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(15,GPIO.OUT)
GPIO.output(15,GPIO.LOW)