# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 14:56:28 2020

@author: Lukas

Class for dataset to allow embedding in GUI
"""

import time
from datetime import timedelta
from copy import deepcopy

# custom datasets
from data.OxData import OxData

# plotting
from skimage.transform import resize
from skimage.io import imshow

class Dataset:
    def __init__(self, name):
       
        ''' creates datasets according to settings, case distinction '''
        self.OxData_DATASETS = [
            "MNIST"
            ] 
        
        ''' specific dataset name + general parameters'''
        self.name = name
        self.dataSize = 500
        '''data transformations:'''        
        kwargs = {'batch_size': args.batch_size}
        
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
    # def plotData(self,fig):
    #     #plotStuff(self.dataset_data_C1, self.dataset_data_C2, self.name,fig)
    #     return 0
        