#!/usr/bin/env python3

from ev3dev.ev3 import *
from math import sin, cos
from time import sleep, time
from writeCSV import WriteCSV
import pickle
import threading
from Ev3devSetup import Ev3devSetup
import socket
import time
import random

buttonValues = {1: "Up", 2: "Down", 3: "Left", 4: "Right"}

# ============================================
# A thread class from https://www.tutorialspoint.com/python/python_multithreading.htm
# This thread class represents a background thread on the robot to collect sensor-motor data and send it back
# to the server.
class SensorBackgroundThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        while True:
            sensorValues(self.name)

#Setting up with MAX_SENSOR, MAX_MOTOR, BIAS, SENSOR_GAIN, OUTPUT_GAIN
ev3devrobot = Ev3devSetup()

motor_left = ev3devrobot.initLargeMotor('outB')
motor_left.reset()

motor_right = ev3devrobot.initLargeMotor('outC')
motor_right.reset()

left_colour_sensor = ev3devrobot.initColorSensor('in2')
left_colour_sensor.mode = 'COL-AMBIENT'

right_colour_sensor = ev3devrobot.initColorSensor('in3')
right_colour_sensor.mode = 'COL-AMBIENT'

left_ultrasonic_sensor = ev3devrobot.initUltraSonicSensor('in1')
left_ultrasonic_sensor.mode = 'US-DIST-CM'

right_ultrasonic_sensor = ev3devrobot.initUltraSonicSensor('in4')
right_ultrasonic_sensor.mode = 'US-DIST-CM'

# ===============================================

def cleanup():
    print('cleaning up...')
    mySocket.close()
    print("Socket closed")
    motor_left.stop()
    motor_right.stop()
    print('quiting')
    exit()


btn = button()

# ===============================================

# Do something when state of any button changes:
def right(state):  # neater use of 'if' follows:
    #global SENSOR_GAIN
    if state:
        ev3devrobot.SENSOR_GAIN += 0.05
        print('SENSOR_GAIN:', ev3devrobot.SENSOR_GAIN)

# ===============================================

def left(state):
    #global SENSOR_GAIN
    if state:
        ev3devrobot.SENSOR_GAIN -= 0.01
        print('SENSOR_GAIN:', ev3devrobot.SENSOR_GAIN)

# ===============================================

def up(state):
    #global OUTPUT_GAIN
    if state:
        ev3devrobot.OUTPUT_GAIN += 0.5
        print('OUTPUT_GAIN:', ev3devrobot.OUTPUT_GAIN)

# ===============================================

def down(state):
    #global OUTPUT_GAIN
    if state:
        ev3devrobot.OUTPUT_GAIN -= 0.1
        print('OUTPUT_GAIN:', ev3devrobot.OUTPUT_GAIN)

# ===============================================

def enter(state):
    print('Enter button pressed' if state else 'Enter button released')

# ===============================================

def backspace(state):
    print('Backspace button pressed' if state else 'Backspace button released')
    cleanup()

# ===============================================

def sensorValues(threadName):

	while True:
		# get random number to determine if the robot is going to move up, down, right or left
		num = random.randrange(4)
		if num == 0:
			pass
		elif num == 1:
			pass
		elif num == 2:
			pass
		elif num == 3:
			pass

# ==============================================

def startNewThread(name):
    # Create a new daemon thread just for taking in sensory-motor values
    thread1 = SensorBackgroundThread(1, "Thread-1", 1)
    thread1.daemon = True
    thread1.start()

host = '192.168.100.17'
port = 5000
global mySocket
print("Creating socket")
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.connect((host, port))
print("Socket connected to {0}".format(host))

print("Starting new thread to send sensor values")
startNewThread('Thread-1')
print("Thread created")

# Check on main thread if the user quits the program
while True:
    k = mySocket.recv(2048).decode()
    if k == 'q':
        break

# Close the socket after the program has quit from the server side
# mySocket.close()
cleanup()


	