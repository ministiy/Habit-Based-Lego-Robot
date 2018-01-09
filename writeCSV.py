#!/usr/bin/env python3

import csv
from pathlib2 import Path

class WriteCSV:

    def __init__(self,filename):
        self.filename = filename
        self.file = None

    def openFile(self):
        fileCheck = Path(self.filename)
        # if file exist, clear the file.
        if fileCheck.is_file():
            self.file = open(self.filename, 'w')
            #file.close()

        self.file = open(self.filename, 'a', newline="")
        #self.file = file

    def closeFile(self):
        self.file.close()
        
    def writeHeader(self):
        header = ['left sensor', 'right sensor', 'left ultraviolet sensor', 'right ultraviolet sensor', 'left motor',
                  'right motor']
        #with open('output.csv', 'w', newline="") as output_file:
        wr = csv.writer(self.file, delimiter=',', quoting=csv.QUOTE_ALL)
        wr.writerow(header)

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