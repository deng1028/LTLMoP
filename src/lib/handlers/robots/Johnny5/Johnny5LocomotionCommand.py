#!/usr/bin/env python
"""
==================================================================
Johnny5LocomotionCommand.py - Johnny5 Locomotion Command Handler
==================================================================

Send commands to Johnny 5.
"""
import math
import time
import logging
import globalConfig

class Johnny5LocomotionCommandHandler:
    def __init__(self, proj, shared_data):
        """
        Locomotion Command handler for Johnny 5 robot.

        proj project obj
        """
        try:
            self.johnny5Serial = shared_data["Johnny5Serial"]
        except:
            print "(LOCO) ERROR: No connection to Johnny 5"
            exit(-1)

    def sendCommand(self, cmd):
        """    Send movement command to Johnny 5
        """
        velGain = 1000
        angGain = 1000
        
        # Angular velocity value
        if cmd[1]!=0 and math.fabs(cmd[1])<0.1:
            cmd[1] = 0.1
        if cmd[1]>0.5:
            cmd[1] = 0.5
        if cmd[1]<-0.5:
            cmd[1] = -0.5
        
        # Velocity value
        if cmd[0]!=0 and math.fabs(cmd[0])<0.1:
            cmd[0] = 0.1
        if cmd[0]>0.3:
            cmd[0] = 0.3
        if cmd[0]<-0.3:
            cmd[0] = -0.3
                        
        # print debugging message
        logging.debug(cmd[1])
        logging.debug(cmd[0])
                
        self.johnny5Serial.write('#15 P%d\r' % (1500-angGain*cmd[1]))
        self.johnny5Serial.write('#14 P%d\r' % (1475-velGain*cmd[0]))
       
