# -*- coding: utf-8 -*-
"""
Created on  15.12.2020

@author: Lukas

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class StreamHandler():
    #data_file = 'sensor-data-60seconds.csv'
    
    def __init__(self, 
                 #root: str, 
                 filePath = 'sensor-data-60seconds.dat',
                 ) -> None:
        
        super().__init__()

        self.filePath = filePath

        # format settings
        self.frameLength = 5
        self.packetLength = 25

        file = open('./data/' + filePath,"rb")

        #with open(path, 'rb') as f:
        #   text = f.read()
        self.file = file

        self.file.read(1) # offset needs to be determined by synchronizeStream method

    def readPacket(self):
        print("STATUS: PLETH: ADDON: CHECK")

        for i in range(0,self.packetLength):
            newFrame = self.readFrame()
            integerList = [newFrame[0], (newFrame[1]<<8)+newFrame[2],newFrame[3], newFrame[4]]
            frameLine = str(integerList)    # PLETH(MSB)*256 + PLETH(LSB)
            CHECK = sum(newFrame[:-1])%256  # verify check sum
            print(frameLine)
            print("CHECK:", CHECK)

    def readFrame(self):
        newFrame = self.file.read(self.frameLength)
        return newFrame

    def synchronizeStream(self):
        # find first frame in package
        return 0

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx:int):
        """
        Args:
            index (int): Index
        Returns:
            tuple: (image, target) where target is index of the target class.
        """
        sample = self.data[idx]

        return sample

def main():
    streamObj = StreamHandler()
    streamObj.readPacket()
    
if __name__ == '__main__':
    main()