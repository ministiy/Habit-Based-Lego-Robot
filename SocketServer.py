#!/usr/bin/env python3

import socket
import termios, tty, sys
import threading
import pickle
from writeCSV import WriteCSV
import Constant

# A thread class from https://www.tutorialspoint.com/python/python_multithreading.htm
# This class represents a background thread used by the server to store collected data into a .csv file
class CSVBackgroundThread (threading.Thread):
   def __init__(self, threadID, name, counter, writer):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.writer = writer
   def run(self):
        # Printing and writing to CSV file
        while True:
            data = conn.recv(4096)
            listOfValues = pickle.loads(data)
            for i in range(Constant.PACKAGE_SIZE):
                print('ls:%0.3f rs:%0.3f lu:%0.3f ru:%0.3f lm:%0.3f rm:%0.3f' % (listOfValues[0], listOfValues[1], listOfValues[2], listOfValues[3], listOfValues[4], listOfValues[5]))
                self.writer.writeData(listOfValues[:6])
                listOfValues = listOfValues[6:]
                #   print(listOfValues)


# ==== CSV FUNCTIONS ==== #
# ==============================================

def startNewThread(name, writer):
    # Create a new daemon thread just for taking in sensory-motor values
    thread1 = CSVBackgroundThread(1, "Thread-1", 1, writer)
    thread1.daemon = True
    thread1.start()

# ==============================================

def openCSVFile():
    writer = WriteCSV('output.csv')
    writer.openFile()
    return writer

# ==============================================

# ==== ROBOT COMMAND FUNCTIONS ==== #
# ==============================================
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    ch = sys.stdin.read(1)
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch


# ==============================================

# Code is based on https://stackoverflow.com/questions/41294848/python-sockets-how-to-connect-between-two-computers-on-the-same-wifi
def Main():

    #This IP address allows it to broadcast it to "all computers" on the network.
    host = ''
    port = 5000

    print("Creating Socket")
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #https://stackoverflow.com/questions/4465959/python-errno-98-address-already-in-use
    mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    mySocket.bind((host, port))
    print("Socket started listening")

    mySocket.listen(1)
    global conn
    conn, addr = mySocket.accept()
    print("Connection established with {0}".format(addr))

    # Setting up the .csv file
    print("Opening output.csv")
    writer = openCSVFile()
    writer.writeHeader()

    # Starting the background thread in order to collect data from the robot
    print('Starting thread to write sensor values to csv files')
    startNewThread('Thread-1', writer)
    print("Thread created")

    # Robot controls on main thread
    # Starting the program on server side (and client side)
    print("Connection from: " + str(addr)) #Here is where we say "Connected to the EV3DEV robot"
    movementType = int(input("1.Keyboard 2.Braitenburg 3.Random"))
    conn.send(str(movementType).encode())
    while True:
        #data = conn.recv(1024).decode()
        #if not data:
        #    break
        #print("from connected  user: " + str(data))

        # data = str(data).upper()

        k = getch()

        print("sending: " + str(k))
        conn.send(k.encode())
        print("Sent")

        if k == 'q':
            break;

    conn.close()
    mySocket.close()
    writer.closeFile()


if __name__ == '__main__':
    Main()

