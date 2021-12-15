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
        self.PackageLength = 25

        file = open('./data/' + filePath,"rb")#

        self.frameSync = False
        self.packageSync = False

        #with open(path, 'rb') as f:
        #   text = f.read()
        self.file = file
        self.file.read(1) # offset needs to be determined by synchronizeStream method
        self.frameSync = True

    def readPackage(self):
        # reads package as list of lists (frames)
        print("STATUS: PLETH: ADDON: CHECK")
        package = []

        for frame in range(0,self.PackageLength):

            # synchronize package
            if not self.packageSync:
                newFrame = self.synchronizeStream()     # returns package starting value. Needs to be handled separatelly due to read pointer position.
            else:
                newFrame = self.readFrame()

            integerList = self.processFrame(newFrame,index=frame+1)
            package.append(integerList)

        print(package)

        return package
            
    def processFrame(self,newFrame,index=1,checkCHK = True,printLine = False):
        # precesses bitstream according to datasheet, validates checksum
        integerList = [index, newFrame[0], (newFrame[1]<<8)+newFrame[2],newFrame[3], newFrame[4]]
        frameLine = str(integerList)        # PLETH(MSB)*256 + PLETH(LSB)

        if checkCHK:
            if not self.checkFrameCHK(newFrame):
                print("ERROR: Checksum of frame number " + str(index) + " not correct.")

        if printLine:
            print(frameLine)
            print("CHECK:", self.checkFrameCHK(newFrame))
            print("STATUS:", newFrame[0] & 1)   # check if LSB of STATUS byte is one to determine first frame of package

        return integerList


    def readFrame(self,nBytes=0):
        if nBytes == 0:
            nBytes = self.frameLength
        newFrame = self.file.read(nBytes)
        return newFrame

    @staticmethod
    def checkFrameCHK(frame):
        # calulates checksum of given frame and compares it with given value
        checkSum = sum(frame[:-1])%256
        return (frame[-1]== checkSum)   # return boolean
 
    def synchronizeStream(self):
        # find first frame in package
        syncBit = 0
        counter = 0
        while(syncBit != 1):
            newFrame = self.readFrame()
            syncBit = (newFrame[0] & 1)
            counter += 1
            if counter == 75:           # TO DO: improve error handling
                print("Package synchronization could not be determined from given Bytes.")
                print("Check frame definition for correct Byte synchronization.")
                break 

        if syncBit == 1:
            print("Packages synchronization successful!")
            self.packageSync = True
        return newFrame

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
    streamObj.readPackage()
    
if __name__ == '__main__':
    main()