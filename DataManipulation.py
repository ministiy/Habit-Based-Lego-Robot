#!/usr/bin/env python3

import csv
import pandas as pd
import numpy as np

class DataManipulation:

    def __init__(self):
        self.__data = pd.read_csv("output.csv")
        self.__NUM_OF_BINS = 10
        self.__total = 0
        self.__total_motor = None
        self.__total_sensor = None
        self.__total_us = None


    def normalized_motor(self):
        self.__data['right motor'] = self.__data['right motor'].values/1000 #min -1 max 1
        self.__data['left motor'] = self.__data['left motor'].values/1000 #min -1 max 1

    def normalized_0_to_1(self):
        self.__total_motor = (0.5*((self.__data['left motor'].values + self.__data['right motor'].values)/2) + 0.5) * self.__NUM_OF_BINS
        self.__total_sensor = ((self.__data['left sensor'].values + self.__data['right sensor'].values) / 2)  * self.__NUM_OF_BINS
        self.__total_us = ((self.__data['left ultrasound sensor'].values + self.__data['right ultrasound sensor'].values) / 2)  * self.__NUM_OF_BINS
        
        for i in range(len(self.__total_motor)):
            if self.__total_motor[i] == self.__NUM_OF_BINS:
                self.__total_motor[i] = self.__NUM_OF_BINS-1
            if self.__total_sensor[i] == self.__NUM_OF_BINS:
                self.__total_sensor[i] == self.__NUM_OF_BINS-1
            if self.__total_motor[i] == self.__NUM_OF_BINS:
                self.__total_motor[i] == self.__NUM_OF_BINS-1

        self.__total_motor = np.floor(self.__total_motor).astype(int)
        self.__total_sensor = np.floor(self.__total_sensor).astype(int)
        self.__total_us = np.floor(self.__total_us).astype(int)

        return self.__total_motor,self.__total_sensor,self.__total_us

    def normalized_minus1_to_1(self):
        pass

    def calculate_total(self, firstDimension=None, secondDimension=None, thirdDimension=None):
        if firstDimension is not None: 
            self.__total += firstDimension 
        if secondDimension is not None:
            self.__total += self.__NUM_OF_BINS * secondDimension
        if thirdDimension is not None:
            self.__total += (self.__NUM_OF_BINS**2) * thirdDimension

        self.__total = np.floor(self.__total).astype(int)
        return self.__total

    def remove_continous_state(self):
        return [self.__total[i] for i in range(len(self.__total)-1) if self.__total[i+1] != self.__total[i]]