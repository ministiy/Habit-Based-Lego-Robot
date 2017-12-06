#!/usr/bin/env python3
# so that script can be run from Brickman

# Note: the code below was copied from the link https://sites.google.com/site/ev3python/learn_ev3_python/keyboard-control
# on Dec, 7th 2017

import termios, tty, sys
from ev3dev.ev3 import *

# attach large motors to ports B and C, medium motor to port A
motor_left = LargeMotor('outB')
motor_right = LargeMotor('outC')
#motor_a = MediumMotor('outA')
motor_left.reset()
motor_right.reset()


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
    motor_left.reset()
    motor_right.reset()
    motor_right.run_timed(speed_sp=450, time_sp=100)
    motor_left.run_timed(speed_sp=450,time_sp=100)




# ==============================================

def back():
    motor_left.run_forever(speed_sp=-450)
    motor_right.run_forever(speed_sp=-450)


# ==============================================

def left():
    motor_left.run_forever(speed_sp=-450)
    motor_right.run_forever(speed_sp=450)


# ==============================================

def right():
    motor_left.run_forever(speed_sp=450)
    motor_right.run_forever(speed_sp=-450)


# ==============================================

def stop():
    motor_left.stop()
    motor_right.stop()


# ==============================================

while True:
    print("Program started")
    k = getch()
    print(k)
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