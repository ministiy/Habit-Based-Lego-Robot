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
    stopMotor()
    print("Motor stopped")
    print('quiting')
    exit()


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

def stopMotor():
    motor_left.stop()
    motor_right.stop()

# ===============================================

def sensorValues(threadName):
    it = 0
    # Get original time as a basis to run the following code every n seconds (where n <= 0.1)
    starttime = time.time()
    buttonValues = {0: "Forward", 1: "Back", 2: "Left", 3: "Right"}
    packageSize = 0
    package = []

    while True:
        it += 1
        lsv = ev3devrobot.SENSOR_GAIN * float(left_colour_sensor.value()) / ev3devrobot.MAX_SENSOR
        rsv = ev3devrobot.SENSOR_GAIN * float(right_colour_sensor.value()) / ev3devrobot.MAX_SENSOR

        luv = 1.0 - max(0.0, min(1.0, float(left_ultrasonic_sensor.value()) / 200.0))
        ruv = 1.0 - max(0.0, min(1.0, float(right_ultrasonic_sensor.value()) / 200.0))

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

        'lmv = motor_left.speed'
        'rmv = motor_right.speed'

        ## AGGR
        lmv = ev3devrobot.BIAS + rsv - 0.0 * lsv - (ruv * 2.)
        rmv = ev3devrobot.BIAS + lsv - 0.0 * rsv - (luv * 2.)

        lmv *= ev3devrobot.OUTPUT_GAIN
        rmv *= ev3devrobot.OUTPUT_GAIN

        if max(lmv, rmv) > ev3devrobot.MAX_MOTOR:
            lmv -= max_mv - ev3devrobot.MAX_MOTOR
            rmv -= max_mv - ev3devrobot.MAX_MOTOR
            # OUTPUT_GAIN *= 0.95
            # print('OUTPUT_GAIN decreased to : %f' %(OUTPUT_GAIN))

        # if min(lmv,rmv) < 0.05 :
        #     OUTPUT_GAIN *= 1.05
        #     print('OUTPUT_GAIN increased to : %f' %(OUTPUT_GAIN))


        if (it % 10) == 0:
            print('ls: %0.3f rs:%0.3f lm: %0.3f rm:%0.3f' % (lsv, rsv, lmv, rmv))

        lmv = int(max(-1000, min(1000, ev3devrobot.MAX_MOTOR * lmv)))
        rmv = int(max(-1000, min(1000, ev3devrobot.MAX_MOTOR * rmv)))

        # get random number to determine if the robot is going to move forward, back, right or left
        num = random.randrange(4)
        if num == 0:
            motor_left.run_timed(speed_sp=450, time_sp=100)
            motor_right.run_timed(speed_sp=450, time_sp=100)
        elif num == 1:
            motor_left.run_timed(speed_sp=-450, time_sp=100)
            motor_right.run_timed(speed_sp=-450, time_sp=100)
        elif num == 2:
            motor_left.run_timed(speed_sp=450, time_sp=100)
            motor_right.run_timed(speed_sp=-450, time_sp=100)
        elif num == 3:
            motor_left.run_timed(speed_sp=-450, time_sp=100)
            motor_right.run_timed(speed_sp=450, time_sp=100)

        '''
        listOfValues = [lsv, rsv, luv, ruv, lmv, rmv]
        dataString = pickle.dumps(listOfValues)
        mySocket.send(dataString)

        time.sleep(0.05 - ((time.time() - starttime) % 0.05))
        '''
        listOfValues = [lsv, rsv, luv, ruv, lmv, rmv]
        package = listOfValues + package
        print(package)

        packageSize += 1
        print(packageSize)
        if packageSize == 10:
            print(package)
            dataString = pickle.dumps(package)
            mySocket.send(dataString)
            packageSize = 0
            package = []

        time.sleep(0.05 - ((time.time() - starttime) % 0.05))

# ==============================================

def startNewThread(name):
    # Create a new daemon thread just for taking in sensory-motor values
    thread1 = SensorBackgroundThread(1, "Thread-1", 1)
    thread1.daemon = True
    thread1.start()

btn = Button()
btn.on_left = left
btn.on_right = right
btn.on_up = up
btn.on_down = down
btn.on_enter = enter
btn.on_backspace = backspace

it = 0
#host = '192.168.1.66'
host = '172.24.9.187'
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


	