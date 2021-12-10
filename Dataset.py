# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 14:56:28 2020

@author: Lukas

Class for dataset to allow embedding in GUI
"""

import matplotlib.pyplot as plt
from copy import deepcopy
import numpy as np

# custom datasets
from data.OxData import OxData

# plotting
#from skimage.transform import resize
#from skimage.io import imshow

class Dataset:
    def __init__(self, name):
       
        ''' creates datasets according to settings, case distinction '''
        self.OxData_DATASETS = [
            "MNIST"
            ] 
        
        ''' specific dataset name + general parameters'''
        self.name = name
        
        ''' type: IMAGE or EEG '''
        if self.name in self.OxData_DATASETS:
            self.datasetType = 'OxData'
            #param = {'translate': [0, 0],'pinkNoise':[1,0,0], 'normalize': True,
            #         'binary': True,'nShuffle': 0,'dimRed': False}
            #transform=transformDataset(param,'MNIST',network,resizeOn)
            
            #self.transform = transform
            
        self.createDatasets()

    def createDatasets(self):
        ''' creates datasets according to settings, case distinction '''
        ''' create dataset '''
        if self.datasetType == "OxData": 
            self.OxData= OxData()
           
    def updateTransformation(self,dataSettings,transformIn):
        transform = deepcopy(transformIn)
        return transform

    # ''' function calls '''
    def plotData(self,fig):

        #xTickArray = np.arange(7)*0.2*128
        #xTickLabels = np.arange(-1,6)*200
        plt.rcParams.update({'font.size': 8})
        # optional thresholding
        # print(dataC1.shape)
        # print(dataC2.shape)
        # dataC1, noisyDataC1 = separateOutliers(dataC1,2.01)
        # dataC2, noisyDataC2 = separateOutliers(dataC2,2.01)
        # print(dataC1.shape)
        # print(dataC2.shape)
        ''' average plot ''' 
        ax = plt.gca()
        plt.setp(ax.spines.values(), linewidth=2)
        #plt.grid(True)

        dataPointer = self.OxData.dataPointer
        window = self.OxData.window
        data = self.OxData.data['PLETH'][dataPointer:dataPointer+window]
        #data = np.random.randint(-2,3,(150,))
        plt.plot(np.arange(0,len(data)),data) #,cmap='viridis')
        #plt.clim(limit_low,limit_high) 
        #plt.set_cmap('viridis')
        plt.title('Pleth signal')
        #plt.xticks(xTickArray,xTickLabels)
        plt.xlabel('time [ms]')
        plt.ylabel('channels')

        # increment data pointer for next window
        self.OxData.dataPointer = dataPointer + window

        return 0
        
    def calculateOx(self):
        return 85