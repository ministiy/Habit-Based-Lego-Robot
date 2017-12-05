#!/usr/bin/env python3
from ev3dev.ev3 import *

m = LargeMotor('outB')
m.run_timed(time_sp=1000, speed_sp=500)
Sound.speak('Welcome to ev3dev project!').wait()
