from ev3dev.auto import *
import time

#Spin the left motor for 3 seconds
m = LargeMotor('outB')
m.run_timed(time_sp=3000, speed_sp=500)
