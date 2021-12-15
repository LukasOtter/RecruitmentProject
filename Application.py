# -*- coding: utf-8 -*-
"""
Created on 10.12.2021

@author: Lukas Otter

GUI based on the tkinter backend that displays a visualization of a datastream 
of a OEM III Pulse Oximetry Module from Nonin

TODO:
- handle file closing

"""

import tkinter as tk
from tkinter import *
from Dataset import Dataset

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from math import floor,ceil
import numpy as np
import time

class Application(tk.Frame):

    def __init__(self, master=None):

        # define color scheme
        self.bgColor = "grey18"     # background color
        self.bdColor = ""           # border color
        self.fgColor = "grey90"           # font color       
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master, bg=self.bgColor)   

        # reference to the master widget, which is the tk window                 
        self.master = master

        # with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

        self.figureHandle = 0
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a menu instance
        menu = Menu(self.master, bg=self.bgColor,fg=self.fgColor)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)

        #added "file" to our menu
        menu.add_cascade(label="File", menu=file)

        # create the file object)
        edit = Menu(menu)

        #added "file" to our menu
        menu.add_cascade(label="Edit", menu=edit)

        # define all window elements and initalize their values
        self.initializeUI()
            
        # create default datsets (first array entry)
        self.dataset =  Dataset(self.datasetName.get())
        #exit()
  
    def initializeUI(self): 

        # add bool for class-specific manipulations
        self.labelframeChange = LabelFrame(self.master, text="Settings:", height = 95, width = 120, bg=self.bgColor,
                                            fg=self.fgColor)
        self.labelframeChange.place(x = 320, y = 525)
        
        # add bars for data manipulation settings
        self.labelframeSettings = LabelFrame(self.master, text="Data visualization", height = 510, width = 704,bg=self.bgColor,
                                                fg=self.fgColor)
        self.labelframeSettings.place(x=10, y=0)
        
        # add button to create data
        self.nextWindow = Button(self, text='Scan data', command=self.create_data,height = 5, width = 27,bg=self.bgColor,
                                                fg=self.fgColor)
        self.nextWindow.place(x = 731, y = 424)
        
        # availabe datasets - add new dataset name here
        DATASETS_OxData = [
            "OxData"
            ]
        self.datasetName = StringVar(self)
        self.datasetName.set(DATASETS_OxData[0]) # default value

        # Evaluation parameters
        self.labelframeHR = LabelFrame(self.master, text="Heart rate:", height = 200, width = 200,bg=self.bgColor,
                                                fg=self.fgColor)
        self.labelframeHR.place(x=730, y=00) 

        self.labelframeSpO2= LabelFrame(self.master, text="SpO2:", height = 200, width = 200,bg=self.bgColor,
                                                fg=self.fgColor)
        self.labelframeSpO2.place(x=730, y=210) 
        
        self.labelHR = Label(self.labelframeHR,bg=self.bgColor,fg=self.fgColor)
        self.labelHR.configure(text = "--",font=("Arial", 30))
        self.labelHR.place(relx = 0.5,rely = 0.5,anchor = 'center')

        self.labelSpO2 = Label(self.labelframeSpO2,bg=self.bgColor,fg=self.fgColor)
        self.labelSpO2.configure(text = "--",font=("Arial", 30))
        self.labelSpO2.place(relx = 0.5,rely = 0.5,anchor = 'center')
        
    # button callbacks
    def create_data(self):
        
        # reset/create canvas
        if self.figureHandle == 0:
            self.figureHandle = Figure(figsize=(7,5), dpi=100)
            self.axesHandle = self.figureHandle.add_subplot(111)
        else:
            #self.figureHandle.clear(True)
            #pass
            #plt.clf()
            #matplotlib.figure.clf()
            self.canvas.destroy()
        
        # reset/create canvas
        try: 
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError: 
            pass 
        
        self.canvas = FigureCanvasTkAgg(self.figureHandle, self.labelframeSettings)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.NONE, expand=False)
        
        self.plotData()


    # helper methods
    def plotData(self):
        # visualizes data from the read file in GUI in a "real-time-like" motion
        # plt.rcParams.update({'font.size': 8})

        dataPointer = 0
        window = self.dataset.OxData.window
        numberOfSamples = self.dataset.OxData.nSamples
        Fs = self.dataset.OxData.Fs

        step = floor(self.dataset.OxData.Fs/3) # one frame 

        # loop which updates the pleth, HR and SpO2
        for dataPointer in range(0,numberOfSamples-window,step):

            # label figure
            xTickArray = np.arange(0,window+Fs,Fs)
            xTickLabels = np.flip(xTickArray/(Fs))
            self.axesHandle.set_xticks(xTickArray , minor=False)
            self.axesHandle.set_xticklabels(xTickLabels, fontdict=None, minor=False)

            self.axesHandle.set_xlabel('time relative to current measurement [s]')
            self.axesHandle.set_ylabel('amplitude')
            self.axesHandle.set_ylim((25000,40000))
            self.axesHandle.grid()

            # extract current frame data
            data = self.dataset.OxData.data['data'][dataPointer:dataPointer+window,4]
            HR = self.dataset.OxData.data['HR'][int(dataPointer/step)]
            SpO2 = self.dataset.OxData.data['SpO2'][int(dataPointer/step)]

            # create line plot
            self.axesHandle.plot(np.arange(0,len(data)),data) #,cmap='viridis')
            self.canvas.draw()

            # update evaluation parameters
            self.updateHR(HR)
            self.updateSpO2(SpO2)
        
            # refresh figure for "real-time" visualization 
            self.axesHandle.clear()
            self.canvas.flush_events()
            time.sleep(0.30)

    # update evaluation parameters 
    def updateHR(self,HR):
        self.labelHR.configure(text = str(HR))

    def updateSpO2(self,newSpO2):
        self.labelSpO2.configure(text = str(newSpO2))
            
def main():
    root = tk.Tk()
    root.geometry("950x520")
    #root.state('zoomed')
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
