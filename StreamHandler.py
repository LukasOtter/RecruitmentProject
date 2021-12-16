# -*- coding: utf-8 -*-
"""
Created on 15.12.2021

@author: Lukas Otter

Class to handle the decoding of .dat file (data format #7)

TODO: 
- implement frame synchronization. So far, the first STATUS Byte in the input file
 is detected using a predefined, file specific offset

- more elegant handling of read operation. Use "with" syntax
"""

import matplotlib.pyplot as plt
import numpy as np

class StreamHandler():

    def __init__(self, 
                 #root: str, 
                 fileName = 'sensor-data-60seconds.dat',
                 ) -> None:
        
        super().__init__()

        self.fileName = fileName
        self.filePath = './data/' + fileName

        # format settings
        self.frameLength = 5
        self.PackageLength = 25

        # indices for data labeling
        self.sampleIndex = 0
        self.packageIndex = 0

        # flags to monitor file synchronization
        self.frameSync = False
        self.packageSync = False

        file = open(self.filePath,"rb")
        
        self.file = file
        self.openFile = True
        #self.file.read(1) # offset needs to be determined by synchronizePackage method
        #self.frameSync = True

    def readStreamFile(self):
        # reads all packages in file

        data = {'data': [],'HR':[],'SpO2':[]}
        package = 0

        # loop through all packages until an incomplete package triggers the file closing
        while self.openFile:
            self.packageIndex += 1
            package = self.readPackage()
            if package != "EOF":
                data['data'] = data['data'] + package['data']
                data['HR'].append(package['HR'])
                data['SpO2'].append(package['SpO2'])

        # convert losts to numpy arrays for easier data handling
        data['data'] = np.asarray(data['data'])
        data['HR'] = np.asarray(data['HR'])
        data['SpO2'] = np.asarray(data['SpO2'])

        print("Decoded data transferred to application!")
        #print(data['data'])

        return data

    def readPackage(self):
        # reads package as list of lists (frames)
        packageData = [] 

        for frame in range(0,self.PackageLength):
            # synchronize package
            tmpFrame = []
            inputFlag = False
            if not self.frameSync:
                newFrame = self.synchronizeFrame()                      # returns package starting value. 
                tmpFrame = newFrame                                     # Needs to be handled separatelly 
                inputFlag = True                                        # due to read pointer position.

            if not self.packageSync:
                newFrame = self.synchronizePackage(tmpFrame,inputFlag)  # returns package starting value. 
                                                                        # Needs to be handled separatelly 
                                                                        # due to read pointer position.
            else:
                newFrame = self.readFrame()

            self.sampleIndex += 1
            integerList = self.processFrame(newFrame,index=frame+1)
            if integerList != "EOF":
                packageData.append(integerList)
            else:
                package = "EOF"
                break

        if self.openFile:
            # post process data to determine HR and SpO2 values
            HR = (packageData[0][5]<<8) + packageData[1][5]  # process heartrate as 16-bit int
            SpO2 = packageData[2][5]

            package = {'data': packageData,'HR': HR,'SpO2': SpO2}

        return package
            
    def processFrame(self,newFrame,index=1,checkCHK = True,printLine = False):
        # precesses bitstream according to datasheet, validates checksum
        if len(newFrame) < self.frameLength:
            integerList = "EOF" 
            self.file.close()
            self.openFile = False

        else:
            # data format #7: SAMPLE, PACKAGE, FRAME, STATUS, PLETH, ADDON, CHECKSUM
            integerList = [self.sampleIndex,self.packageIndex, index, newFrame[0], 
                            (newFrame[1]<<8)+newFrame[2],newFrame[3], newFrame[4]]
            frameLine = str(integerList)        # PLETH(MSB)*256 + PLETH(LSB)

            if checkCHK:
                if not self.checkFrameCHK(newFrame):
                    print("ERROR: Checksum of frame number " + str(index) + " not correct.")

            if printLine:
                print(frameLine)
                print("CHECK:", self.checkFrameCHK(newFrame))
                print("STATUS:", newFrame[0] & 1)   # check if LSB of STATUS byte is one to determine 
                                                    # first frame of package

        return integerList

    def readFrame(self):
        # reads one frame from file
        nBytes = self.frameLength
        newFrame = self.file.read(nBytes)
        return newFrame

    @staticmethod
    def checkFrameCHK(frame):
        # calulates checksum of given frame and compares it with given value
        checkSum = sum(frame[:-1])%256
        return (frame[-1]== checkSum)   # return boolean
 
    def synchronizePackage(self,newFrame=[],inputFlag=False):
        # finds first complete frame in package
        syncBit = 0
        counter = 0
        while(syncBit != 1):
            if not inputFlag: 
                newFrame = self.readFrame()
            else:
                inputFlag = False

            syncBit = (newFrame[0] & 1) # bitwise comparison with one to check LSB of status Byte
            counter += 1
            if counter == 75:           # TO DO: improve error handling
                print("Package synchronization not successful with given Bytes.")
                print("Check package definition for correct synchronization.")
                break 

        if syncBit == 1:
            print("Packages synchronization successful!")
            self.packageSync = True
        return newFrame                 # frame is returned since the read method cannot go back in file

    def synchronizeFrame(self):
        # finds first complete frame in package
        syncBit = 0
        counter = 0
        
        newFrame = self.readFrame()
        
        checkSum = self.checkFrameCHK(newFrame)

        while(checkSum != True):
            newByte = self.file.read(1)
            newFrame = newFrame + newByte
            newFrame = newFrame[1:]
            checkSum = self.checkFrameCHK(newFrame)
            counter += 1
            if counter == 25:           # TO DO: improve error handling
                print("Byte synchronization not successful with given Bytes.")
                print("Check frame definition for correct synchronization.")
                break 

        if checkSum:
            print("Frame synchronization successful!")
            self.frameSync = True
        return newFrame                 # frame is returned since the read method cannot go back in file