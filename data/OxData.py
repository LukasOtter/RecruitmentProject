# -*- coding: utf-8 -*-
"""
Created on 10.12.2021

@author: Lukas Otter

Specific class for the oxygen saturation data and its formatting

"""

import matplotlib.pyplot as plt
import numpy as np

# custom classes
from StreamHandler import StreamHandler

class OxData():
    data_file = 'sensor-data-60seconds.csv'
    
    def __init__(self, 
                 #root: str, 
                 file = 'sensor-data-60seconds.csv',
                 ) -> None:
        
        super().__init__()

        self.dataType = "OxData"
        self.file = file
        
        self.dataPointer = 0      # pointer to reference different samples
        self.Fs = 75              # sampling frequency (3 packages)
        self.window = 5*self.Fs   # 5 second window (15 packages)

        # simpler version with .csv input
        #data_path = './data/' + file
        #self.data = pd.read_csv('./data/' + file,sep = ";")

        streamObj = StreamHandler(fileName='sensor-data-60seconds.dat')
        self.data = streamObj.readStreamFile()

        self.nSamples = len(self.data['HR'])*25

