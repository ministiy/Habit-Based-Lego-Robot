#!/usr/bin/env python3
# so that script can be run from Brickman

# Note: the code below was copied from the link https://sites.google.com/site/ev3python/learn_ev3_python/keyboard-control
# on Dec, 7th 2017

import termios, tty, sys
from ev3dev.ev3 import *
import csv
import threading


MAX_SENSOR = 100.0 # percent
MAX_MOTOR = 1000.0

BIAS = 0.05
SENSOR_GAIN = 1.0
OUTPUT_GAIN = 1.0

# attach large motors to ports B and C
motor_left = LargeMotor('outB')
motor_right = LargeMotor('outC')

motor_left.reset()
motor_right.reset()

ls = ColorSensor('in2')
#assert ls.connected, "Left sensor not connected to port 2"
rs = ColorSensor('in3')
#assert rs.connected, "Right sensor not connected to port 3"
ls.mode='COL-AMBIENT'
rs.mode='COL-AMBIENT'

lu = UltrasonicSensor('in1')
lu.mode='US-DIST-CM'
ru = UltrasonicSensor('in4')
ru.mode='US-DIST-CM'

# ==============================================

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    ch = sys.stdin.read(1)
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch


# ==============================================

#def fire():
#    motor_a.run_timed(time_sp=3000, speed_sp=600)


# ==============================================

def forward():
    motor_right.run_timed(speed_sp=450, time_sp=100)
    motor_left.run_timed(speed_sp=450,time_sp=100)

# ==============================================

def back():
    motor_right.run_timed(speed_sp=-450, time_sp=100)
    motor_left.run_timed(speed_sp=-450, time_sp=100)


# ==============================================

def left():
    motor_right.run_timed(speed_sp=450, time_sp=100)
    motor_left.run_timed(speed_sp=-450, time_sp=100)


# ==============================================

def right():
    motor_right.run_timed(speed_sp=-450, time_sp=100)
    motor_left.run_timed(speed_sp=450, time_sp=100)


# ==============================================

def stop():
    motor_left.stop()
    motor_right.stop()


# ==============================================

def controls():
    while True:
        k = getch()
        #    print(k)
        if k == 'w':
            forward()
        if k == 's':
            back()
        if k == 'a':
            left()
        if k == 'd':
            right()
    #    if k == 'f':
    #        fire()
        if k == 'p':
            stop()
        if k == 'q':
            exit()



# ==============================================

def sensor_values():

    nextthread = threading.Timer(1.0, sensor_values())
    nextthread.daemon = True
    nextthread.start()

    ## normalized to lie between 0 and 1 (1 close, 0 far)
    lsv = SENSOR_GAIN * float(ls.value()) / MAX_SENSOR
    rsv = SENSOR_GAIN * float(rs.value()) / MAX_SENSOR

    luv = 1.0 - max(0.0, min(1.0, float(lu.value()) / 200.0))
    ruv = 1.0 - max(0.0, min(1.0, float(ru.value()) / 200.0))

    Leds.set(Leds.LEFT, brightness_pct=lsv)
    Leds.set(Leds.RIGHT, brightness_pct=rsv)

    # if max(lsv,rsv) < 0.1 :
    #     SENSOR_GAIN *=1.05
    #     print('SENSOR_GAIN increased to : %f' %(SENSOR_GAIN))
    # elif min(lsv,rsv) > 0.5 :
    #     SENSOR_GAIN *=0.95
    #     print('SENSOR_GAIN decreased to : %f' %(SENSOR_GAIN))

    # ## LOVE + AGGR
    # lmv = BIAS + (rsv-0.2*lsv)
    # rmv = BIAS + (lsv-0.2*rsv)

    lmv = motor_left.speed
    rmv = motor_right.speed


    # writing to a csv file called output.csv to store sensory-motor data where
    #   lsv = left colour sensor value
    #   rsv = right colour sensor value
    #   luv = left ultraviolet sensor value
    #   ruv = right ultraviolet sensor value
    #   lmv = left motor value
    #   rmv = right motor value
    with open('output.csv', 'a', newline="") as output_file:
        wr = csv.writer(output_file, delimiter=',', quoting=csv.QUOTE_ALL)
        wr.writerow([lsv, rsv, luv, ruv, lmv, rmv])
    print('ls:%0.3f rs:%0.3f lu:%0.3f ru:%0.3f lm:%0.3f rm:%0.3f' % (lsv, rsv, luv, ruv, lmv, rmv))

# ==============================================


header = ['left sensor','right sensor' , 'left ultraviolet sensor' , 'right ultraviolet sensor' , 'left motor', 'right motor']
with open('output.csv', 'w', newline="") as output_file:
        wr = csv.writer(output_file,delimiter = ',' , quoting = csv.QUOTE_ALL)
        wr.writerow(header)

print("Program started")

exitFlag = 0

# A thread class from https://www.tutorialspoint.com/python/python_multithreading.htm
class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      sensor_values()

# Create a new daemon thread just for taking in sensory-motor values
thread1 = myThread(1, "Thread-1", 1)
thread1.daemon = True
thread1.start()

# Control the robot using the main thread
controls()
print ("Exiting program")

