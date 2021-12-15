# -*- coding: utf-8 -*-
"""
Created on 10.12.2021

@author: Lukas Otter

Class for dataset to allow embedding in GUI
"""

import matplotlib.pyplot as plt
import numpy as np

# custom classes
from data.OxData import OxData
from StreamHandler import StreamHandler

class Dataset:
    def __init__(self, name):
       
        # creates datasets according to settings, case distinction
        self.OxData_DATASETS = [
            "OxData"
            ] 
        
        # pecific dataset name + general parameters
        self.name = name
        
        # type: IMAGE or EEG
        if self.name in self.OxData_DATASETS:
            self.datasetType = 'OxData'
                      
        self.createDatasets()

    def createDatasets(self):
        # creates datasets according to settings, case distinction
        # create dataset
        if self.datasetType == "OxData": 
            self.OxData= OxData()
            
