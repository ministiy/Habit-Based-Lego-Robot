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

exitFlag = 1

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

# ============================================
# A thread class from https://www.tutorialspoint.com/python/python_multithreading.htm
# This thread class represents a background thread on the robot to check if the program has quit or not
class ExitBackgroundThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        while True:
            k = mySocket.recv(2048).decode()
            if k == 'q':
                global exitFlag
                exitFlag = 0

# =============================================

# commented this out to reduce annoying beep
# Sound.beep()

MAX_SENSOR = 100.0  # percent
MAX_MOTOR = 1000.0

BIAS = 0.05
SENSOR_GAIN = 1.0
OUTPUT_GAIN = 1.0

Leds.set_color(Leds.LEFT, Leds.YELLOW)
Leds.set_color(Leds.RIGHT, Leds.YELLOW)

"""
lm = LargeMotor('outB')
rm = LargeMotor('outC')
lm.reset()
rm.reset()
b = Button()

ls = ColorSensor('in2')
# assert ls.connected, "Left sensor not connected to port 2"
rs = ColorSensor('in3')
# assert rs.connected, "Right sensor not connected to port 3"
ls.mode = 'COL-AMBIENT'
rs.mode = 'COL-AMBIENT'

lu = UltrasonicSensor('in1')
lu.mode = 'US-DIST-CM'
ru = UltrasonicSensor('in4')
ru.mode = 'US-DIST-CM'
"""

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
    motor_left.stop()
    motor_right.stop()
    print('quiting')
    exit()


btn = Button()

# ===============================================

# Do something when state of any button changes:
def right(state):  # neater use of 'if' follows:
    global SENSOR_GAIN
    if state:
        SENSOR_GAIN += 0.05
        print('SENSOR_GAIN:', SENSOR_GAIN)

# ===============================================

def left(state):
    global SENSOR_GAIN
    if state:
        SENSOR_GAIN -= 0.01
        print('SENSOR_GAIN:', SENSOR_GAIN)

# ===============================================

def up(state):
    global OUTPUT_GAIN
    if state:
        OUTPUT_GAIN += 0.5
        print('OUTPUT_GAIN:', OUTPUT_GAIN)

# ===============================================

def down(state):
    global OUTPUT_GAIN
    if state:
        OUTPUT_GAIN -= 0.1
        print('OUTPUT_GAIN:', OUTPUT_GAIN)

# ===============================================

def enter(state):
    print('Enter button pressed' if state else 'Enter button released')

# ===============================================

def backspace(state):
    print('Backspace button pressed' if state else 'Backspace button released')
    cleanup()

# ===============================================

def sensorValues(threadName):

    # Get original time as a basis to run the following code every n seconds (where n <= 0.1)
    starttime = time.time()
    'exitFlag = 0'

    while True:
        'if exitFlag:'
        '   threadName.exit()'
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
        dataString = pickle.dumps(listOfValues)
        mySocket.send(dataString)

        time.sleep(0.05 - ((time.time() - starttime) % 0.05))

# ==============================================

def startNewThread(name):
    # Create a new daemon thread just for taking in sensory-motor values
    thread1 = SensorBackgroundThread(1, "Thread-1", 1)
    thread1.daemon = True
    thread1.start()

# ==============================================

def startNewExitThread(name):
    # Create a new daemon thread just for checking if user has quit the program
    thread2 = ExitBackgroundThread(1, "Thread-Exit", 1)
    thread2.daemon = True
    thread2.start()

# ==============================================

btn.on_left = left
btn.on_right = right
btn.on_up = up
btn.on_down = down
btn.on_enter = enter
btn.on_backspace = backspace

target_ips = 0.1
start_time = time.time()

it = 0

"""""
# Initialize the class for writing CSV
writer = WriteCSV('output.csv')
writer.writeHeader()
"""

#Host IP is IPv4 address of the computer found by Connection Information on Linux
host = '192.168.1.69'
port = 5000
global mySocket
print("Creating socket")
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.connect((host, port))
print("Socket connected to {0}".format(host))

print("Starting new thread to send sensor values")
startNewThread('Thread-1')
print("Sensor thread created")
startNewExitThread('Thread-Exit')
print("Exit thread created")

'try:'
'output_file = writer.openFile()'



while True:

    if exitFlag == 0:
        break

    it += 1
    t = target_ips * it

    ## normalized to lie between 0 and 1 (1 close, 0 far)
    lsv = SENSOR_GAIN * float(left_colour_sensor.value()) / MAX_SENSOR
    rsv = SENSOR_GAIN * float(right_colour_sensor.value()) / MAX_SENSOR

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

    ## AGGR
    lmv = BIAS + rsv - 0.0 * lsv - (ruv * 2.)
    rmv = BIAS + lsv - 0.0 * rsv - (luv * 2.)

    lmv *= OUTPUT_GAIN
    rmv *= OUTPUT_GAIN

    if max(lmv, rmv) > MAX_MOTOR:
        lmv -= max_mv - MAX_MOTOR
        rmv -= max_mv - MAX_MOTOR
        # OUTPUT_GAIN *= 0.95
        # print('OUTPUT_GAIN decreased to : %f' %(OUTPUT_GAIN))

    # if min(lmv,rmv) < 0.05 :
    #     OUTPUT_GAIN *= 1.05
    #     print('OUTPUT_GAIN increased to : %f' %(OUTPUT_GAIN))

    """""
    if (it % 10) == 0:
        print('ls: %0.3f rs:%0.3f lm: %0.3f rm:%0.3f' % (lsv, rsv, lmv, rmv))
    """

    lmv = int(max(-1000, min(1000, MAX_MOTOR * lmv)))
    rmv = int(max(-1000, min(1000, MAX_MOTOR * rmv)))

    motor_left.run_forever(speed_sp=lmv)
    motor_right.run_forever(speed_sp=rmv)

    """""
    sensor_motor_values = [lsv, rsv, luv, ruv, lmv, rmv]
    writer.writeData(sensor_motor_values, output_file)
    """
    btn.process()  # Check for currently pressed buttons.

    it_duration = time.time() - start_time
    sleep_duration = max(0.0, target_ips - it_duration)
    sleep(sleep_duration)
    if (it % 50 == 0):
        print('it dur: %f  (slept for %f)' % (time.time() - start_time, sleep_duration))

    start_time = time.time()

'finally:'
'writer.closeFile(output_file)'
# Close the socket after the program has quit from the server side
mySocket.close()

