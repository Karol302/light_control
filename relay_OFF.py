#!/usr/bin/env python

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
#GPIO.setup(32,GPIO.OUT)
GPIO.output(32,GPIO.HIGH)
