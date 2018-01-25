#!/usr/bin/env python3

import csv
import pandas as pd

class DataManipulation:

    def __init__(self):
        self.data = pd.read_csv("output.csv")
        self.NUM_OF_BINS = 10

    def normalized_0_to_1(self):
        self.data['right motor'] = self.data['right motor'].values/1000 #min -1 max 1
        self.data['left motor'] = self.data['left motor'].values/1000 #min -1 max 1
        total_motor = (0.5*((self.data['left motor'].values + self.data['right motor'].values)/2) + 0.5) * self.NUM_OF_BINS
        total_sensor = ((self.data['left sensor'].values + self.data['right sensor'].values) / 2)  * self.NUM_OF_BINS
        total_us = ((self.data['left ultrasound sensor'].values + self.data['right ultrasound sensor'].values) / 2)  * self.NUM_OF_BINS
        return total_motor,total_sensor,total_us
    def normalized_minus1_to_1(self):
        pass