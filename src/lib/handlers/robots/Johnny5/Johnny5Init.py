#!/usr/bin/env python
"""
================================================================================
Johnny5Init.py -- Johnny 5 Initialization Handler
================================================================================
Some notes about Johnny 5:
    Servo - 0   base rotates
            1   lower waist leans forwards/backwards
            2   upper waist leans forwards/backwards
            3   left shoulder rotates
            4   left shoulder moves inwards/outwards
            5   left arm rotates
            6   left arm moves inwards/outwards
            7   left hand grasps
            8   right shoulder rotates
            9   right shoulder moves inwards/outwards
            10  right arm rotates
            11  right arm moves inwards/outwards
            12  left hand grasps
            13  head rotates
            14  track moves forwards/backwards  static @ 1500; forward @ <1500; backwards @ >1500; 
            15  track rotates   static @ 1500; CW @ >1500; CCW @ <1500;
    
    Servo commands format: #'Servo Num' + P'Servo Val' + T'Time in ms' + \r
"""

"""
TODO:
    
    
"""
import os
import serial

class initHandler:
    #Defaults
    baud = 115200
    timeout = 1         #in seconds
    
    def __init__(self, proj, comPort):
        """
        The initialization for Johnny 5
        
        comPort (string): The comport to connect to (default='/dev/tty.usbserial-A600eIiI')
        """
        self.johnny5Serial = None   #serial port to Johnny 5      
        
        try:
            self.johnny5Serial = serial.Serial(port = comPort, baudrate =
                                           self.baud, timeout = self.timeout)
        except:
            print ("(INIT) ERROR: Couldn't connect to Johnny 5")
            exit(-1)

        self.config = self.initConfig(os.path.join(os.path.dirname(__file__),'ConfigSSC32.cfg'))
        self.setDefaultPosition()

    def Stop(self):
        print "(INIT) Shutting down serial port!"
        self.johnny5Serial.close()
    
    def initConfig(self, cfgFileName):
        """
            Reads in default configuration file and saves.
            
            8 lines of data for each servo, 16 servos for Johnny 5,
            so index of data ranges from 1-128.
            In each data set of a servo, only lines 4-8 are of interests:
            
            4: servo value at neutral position
            5: Min servo value
            6: Max servo value
            7: Min servo degree
            8: Max servo degree
            
            Generate a 2D array "config" in the following format:
            
            index: 0         1          2         3         4          5
            #servo(0) Neutral_ servo Min_servo Max_servo Min_degree Max_degree
            #servo(1) ...
            .
            .
            .
        """
        cfg = [data.strip('\r\n') for data in open(cfgFileName)]
        # config is a 16x6 array, initialized with all 0
        config = [[0 for i in range(6)] for j in range(16)]
        for i in range(128):
            if i%8==3:
                config[i/8][0] = i/8
                config[i/8][1] = int(cfg[i])
            if i%8==4:
                config[i/8][2] = int(cfg[i])
            if i%8==5:
                config[i/8][3] = int(cfg[i])
            if i%8==6:
                config[i/8][4] = int(cfg[i])
            if i%8==7:
                config[i/8][5] = int(cfg[i])
        
        return config
    
    def setDefaultPosition(self):
        """
        Set Johnny 5 servos to default positions
        """
        time = 1000
        # for servo# 0-15
        for i in range(16):
            self.johnny5Serial.write('#%d P%d T%d\r' % (i, int(self.config[i][1]), time))
        
    def getSharedData(self):
        """
        Return a dictionary of any objects that will need to be shared with
        other handlers
        """
        return {"Johnny5Serial":self.johnny5Serial,
                "DefaultConfig":self.config}
