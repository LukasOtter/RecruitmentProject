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
            dataset_OxData = self.createOxDataDataset()
            self.dataset_OxData = dataset_OxData
                
    # def updateDatasets(self,dataSettings,name,transformOn):
    #     ''' updates transform parameters + datasize '''
    #     self.name = name
  
    #     if self.datasetType == "Image":
    #         if self.name == 'MNIST':   
    #             if transformOn[0] is True:
    #                 transform = self.updateTransformation(dataSettings,self.transform_C1)
    #                 self.transform_C1 = transform
    #                 self.updateDataSettings(dataSettings,'C1')
    #             if transformOn[1] is True:    
    #                 transform = self.updateTransformation(dataSettings,self.transform_C2)
    #                 self.transform_C2 = transform
    #                 self.updateDataSettings(dataSettings,'C2')
    #     elif self.datasetType == "EEG":
    #         if self.name in self.EEG_DATASETS:
    #             transform = self.updateTransformation(dataSettings,self.transform)
    #             self.updateDataSettings(dataSettings,'C1')
    #             self.updateDataSettings(dataSettings,'C2')
    #             self.transform = transform
    #             #print(transform)
            
    #     self.createDatasets()
           
    def updateTransformation(self,dataSettings,transformIn):
        transform = deepcopy(transformIn)
        return transform
    
    ''' separated OxData build method '''
    def createOxDataDataset(self):
        ###
        dataset = OxData()
        return dataset
    
    # def updateDataSettings(self,dataSettings):     
    #     self.dataSettings = dataSettings    
        
    # def returnDataSettings(self):
    #     dataSettings = 1 #self.dataSettingsC2['class ratio']  
    #     return dataSettings

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
        plt.plot(np.arange(0,150),np.random.randint(-2,3,(150,))) #,cmap='viridis')
        #plt.clim(limit_low,limit_high) 
        #plt.set_cmap('viridis')
        plt.title('Pleth signal')
        #plt.xticks(xTickArray,xTickLabels)
        plt.xlabel('time [ms]')
        plt.ylabel('channels')

        return 0
        
    def calculateOx(self):
        return 85