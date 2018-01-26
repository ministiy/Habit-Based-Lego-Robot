#!/usr/bin/env python3

import csv
from pathlib2 import Path

class WriteCSV:

    def __init__(self,filename):
        self.filename = filename
        self.file = None

    def openFile(self):

        # if file exist, clear the file.
        fileCheck = Path(self.filename)
        if fileCheck.is_file():
            self.file = open(self.filename, 'w')

        # open file with append command, so that it does not overwrite everytime we want to write to the file.
        self.file = open(self.filename, 'a', newline="")

    def closeFile(self):
        self.file.close()
        
    def writeHeader(self):
        header = ['left sensor', 'right sensor', 'left ultrasound sensor', 'right ultrasound sensor', 'left motor',
                  'right motor']
        wr = csv.writer(self.file, delimiter=',', quoting=csv.QUOTE_ALL)
        wr.writerow(header)
        self.file.flush() # So the write to csv is not put into buffer.

    def writeData(self, sensor_motor_values):
        # writing to a csv file called output.csv to store sensory-motor data where
            #   lsv = left colour sensor value
            #   rsv = right colour sensor value
            #   luv = left ultraviolet sensor value
            #   ruv = right ultraviolet sensor value
            #   lmv = left motor value
            #   rmv = right motor value
        wr = csv.writer(self.file, delimiter = ',' , quoting=csv.QUOTE_ALL)
        wr.writerow(sensor_motor_values)
        self.file.flush() # So the write to csv is not put into buffer.