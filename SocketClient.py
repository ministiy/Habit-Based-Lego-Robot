import socket
from ev3dev.ev3 import *
import pickle


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

# Code is based on https://stackoverflow.com/questions/41294848/python-sockets-how-to-connect-between-two-computers-on-the-same-wifi
def Main():

    #Host IP is IPv4 address of the computer found by Connection Information on Linux
    host = '192.168.1.73'
    port = 5000

    mySocket = socket.socket()
    mySocket.connect((host, port))

    #message = input(" -> ")

    while True: #message != 'q':
        #mySocket.send(message.encode())

        k = mySocket.recv(1024).decode()

        print('Received from server: ' + k)
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

        #message = input(" -> ")
        listOfValues = [1,2,3,4]
        dataString = pickle.dump(listOfValues)
        mySocket.send(dataString.encode())

    mySocket.close()


if __name__ == '__main__':
    Main()
