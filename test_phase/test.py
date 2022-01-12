#!/usr/bin/env python //if everything is ok, that will return a lux reading from the sensor
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from bh1750 import BH1750
if __name__ == "__main__": 
   tsl = BH1750(debug=True)
   print(tsl.lux())
