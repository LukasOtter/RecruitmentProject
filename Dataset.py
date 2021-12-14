# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 14:56:28 2020

@author: Lukas

Class for dataset to allow embedding in GUI
"""

import matplotlib
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
