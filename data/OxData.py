# -*- coding: utf-8 -*-
"""
Created on  10.12.2020

@author: Lukas

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class OxData():
    data_file = 'sensor-data-60seconds.csv'
    
    def __init__(self, 
                 #root: str, 
                 file = 'sensor-data-60seconds.csv',
                 ) -> None:
        
        super().__init__()

        self.dataType = "OxData"
        self.file = file

        # pointer to reference different samples
        self.dataPointer = 0

        #data_path = './data/' + file

        self.data = pd.read_csv('./data/' + file)
        self.data.head()

        # add code to load data into pandas dataframe

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