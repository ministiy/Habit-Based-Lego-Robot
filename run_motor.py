from ev3dev.auto import *
import time

#Spin the left motor for 3 seconds
m = LargeMotor('outB')
n = LargeMotor('outC')

m.run_timed(time_sp=500, speed_sp=500)
n.run_timed(time_sp=500, speed_sp=500)

