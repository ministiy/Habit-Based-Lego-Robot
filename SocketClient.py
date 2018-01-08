#!/usr/bin/env python3

import socket
from ev3dev.ev3 import *
import pickle
import threading
from Ev3devSetup import Ev3devSetup
import time
from time import sleep, time

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

# =============================================

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

"""
# Setting up constants and variables before actually starting up the program
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
"""
# ==== ROBOT MOVEMENT FUNCTIONS === #
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

# ==== DATA COLLECTION FUNCTIONS ==== #
# ==============================================

def sensorValues(threadName):

    # Get original time as a basis to run the following code every n seconds (where n <= 0.1)
    starttime = time.time()
    exitFlag = 0

    while True:
        ## normalized to lie between 0 and 1 (1 close, 0 far)
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

        lmv = motor_left.speed
        rmv = motor_right.speed


        # writing to a csv file called output.csv to store sensory-motor data where
        #   lsv = left colour sensor value
        #   rsv = right colour sensor value
        #   luv = left ultraviolet sensor value
        #   ruv = right ultraviolet sensor value
        #   lmv = left motor value
        #   rmv = right motor value
        #sensor_motor_values = [lsv, rsv, luv, ruv, lmv, rmv]
        #writer.writeData(sensor_motor_values)

        #with open('output.csv', 'a', newline="") as output_file:
            #wr = csv.writer(output_file, delimiter=',', quoting=csv.QUOTE_ALL)
            #wr.writerow([lsv, rsv, luv, ruv, lmv, rmv])
        #print('ls:%0.3f rs:%0.3f lu:%0.3f ru:%0.3f lm:%0.3f rm:%0.3f' % (lsv, rsv, luv, ruv, lmv, rmv))

        # Time period to wait until new sensor values are taken. Currently values are taken every 0.05 seconds.
        # To change this, change X in
        #   time.sleep(X - ((time.time() - starttime) % X))

        listOfValues = [lsv, rsv, luv, ruv, lmv, rmv]
        #print(listOfValues)
        dataString = pickle.dumps(listOfValues)
        mySocket.sendall(dataString)

        time.sleep(0.05 - ((time.time() - starttime) % 0.05))

# ==============================================

def startNewThread(name):
    # Create a new daemon thread just for taking in sensory-motor values
    thread1 = SensorBackgroundThread(1, "Thread-1", 1)
    thread1.daemon = True
    thread1.start()

# ==============================================

# Code is based on https://stackoverflow.com/questions/41294848/python-sockets-how-to-connect-between-two-computers-on-the-same-wifi
def Main():
    '''
    #Host IP is IPv4 address of the computer found by Connection Information on Linux
    #host = '192.168.1.66'
    host = '172.24.38.156'
    port = 5000
    global mySocket
    print("Creating socket")
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((host, port))
    print("Socket connected to {0}".format(host))

    print("Starting new thread to send sensor values")
    startNewThread('Thread-1')
    print("Thread created")

    # Commands received from the server are translated into actual robot movements
    while True:
        k = mySocket.recv(2048).decode()

        #print('Received from server: ' + k, flush=True)

        if k == 'w':
            forward()
        if k == 's':
            back()
        if k == 'a':
            left()
        if k == 'd':
            right()
        if k == 'p':
            stop()

        if k == 'q':
            break

    # Close the socket after the program has quit from the server side
    mySocket.close()
    '''
    # Host IP is IPv4 address of the computer found by Connection Information on Linux
    # host = '192.168.1.66'
    host = '172.24.38.156'
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
        print(k, flush=True)
        if k == 'q':
            break
    mySocket.close()

if __name__ == '__main__':
    Main()
