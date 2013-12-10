#!/usr/bin/env python
"""
=============================================================
Johnny5Actuator.py - Johnny 5 Robot Actuator Handler
=============================================================
"""
import os
import time

class Johnny5ActuatorHandler:
    def __init__(self, proj, shared_data):
        """
        Johnny 5 Robot Actuator Handler
        """
        self.johnny5Serial = shared_data["Johnny5Serial"]
        self.config = shared_data["DefaultConfig"]
    
    def convertConfig(self, csvFileName):
        """
        .csv file is exported form Sequencer project
        Useful data start from second row
        Column 3:18 shows corresponding servo degree(servo #0-15)
        Column 35:50 shows corresponding servo time(servo #0-15)
        
        Generate servo commands in format:
        #'Servo Num' + P'Servo Val' + T'Time in ms' + \r
        
        Between each step, sleep for maximum servo Time in that step sequence
        """
        config = self.config
        move = [data.strip('\r\n') for data in open(csvFileName)]
        # Convert .csv file into 2D array "move"
        for i in range(len(move)):
            move[i] = move[i].split(';')
        #print(move)
        valid = 0
        for i in range(1,len(move)):
            # Servo num in column 3:18, corresponding Time in column 35:50
            for j in range(3,19):
                valid = 1
                value = config[j-3][2]+(((float(move[i][j]))-config[j-3][4])/(config[j-3][5]-config[j-3][4])*(config[j-3][3]-config[j-3][2]))
                self.johnny5Serial.write('#%d P%d T%d\r' % ((j-3), int(value), int(move[i][j-3+35])))
            # column 35:50 are corresponding servo time in ms
            # [a:b] goes from a to b-1, b not included
            if valid:
                time.sleep(int(max(move[i][35:51]))/1000)
                valid = 0

    #####################################
    ### Available actuator functions: ###
    #####################################

    def standUp(self, actuatorVal, initial=False):
        """
        Stand up with all servos set to default position
        """
        if initial:
            pass
        else:
            if actuatorVal == True:
                
                self.convertConfig(os.path.join(os.path.dirname(__file__),'StandUp.csv'))
            else:
                pass

    def takeBow(self, actuatorVal, initial=False):
        """
        Take a bow if actuatorVal is true
        """
        if initial:
            pass
        else:
            if actuatorVal == True:
                self.convertConfig(os.path.join(os.path.dirname(__file__),'TakeBow.csv'))
            else:
                pass

    def highFive(self, actuatorVal, initial=False):
        """
        High five if actuatorVal is true
        """
        if initial:
            pass
        else:
            if actuatorVal == True:
                self.convertConfig(os.path.join(os.path.dirname(__file__),'HighFive.csv'))
            else:
                self.convertConfig(os.path.join(os.path.dirname(__file__),'StandUp.csv'))
