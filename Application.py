# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 14:06:37 2020

@author: Lukas

GUI to viszualize datasets and their manipulated versions

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
    # def __init__(self, master=None):
    #     super().__init__(master)
    #     self.master = master
    #     self.pack()
    #     self.create_widgets()

    # def create_widgets(self):
    #     self.hi_there = tk.Button(self)
    #     self.hi_there["text"] = "Hello World\n(click me)"
    #     self.hi_there["command"] = self.say_hi
    #     self.hi_there.pack(side="top")

    #     self.quit = tk.Button(self, text="QUIT", fg="red",
    #                           command=self.master.destroy)
    #     self.quit.pack(side="bottom")

    # def say_hi(self):
    #     print("hi there, everyone!")
        
        
     # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):

        # define color scheme
        self.bgColor = "grey18"     # background color
        self.bdColor = ""           # border color
        self.fgColor = "grey90"           # font color       
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master, bg=self.bgColor)   

        #reference to the master widget, which is the tk window                 
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

       #self.figureHandle = plt.figure(facecolor="white")
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

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        #file.add_command(label="Exit", command=self.client_exit)

        #added "file" to our menu
        menu.add_cascade(label="File", menu=file)

        # create the file object)
        edit = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        edit.add_command(label="Undo")

        #added "file" to our menu
        menu.add_cascade(label="Edit", menu=edit)

        ''' define all window elements and initalize their values '''
        self.initializeUI()
            
        ''' create default datsets (first array entry) '''
        self.dataset =  Dataset(self.datasetName.get())
        #exit()
  
    def initializeUI(self): 

        ''' add bool for class-specific manipulations '''
        self.labelframeChange = LabelFrame(self.master, text="Settings:", height = 95, width = 120, bg=self.bgColor,
                                            fg=self.fgColor)
        self.labelframeChange.place(x = 320, y = 525)
        
        self.change_C1 = tk.BooleanVar(self)
        self.change_C2 = tk.BooleanVar(self)
        self.change_C1.set(True)
        self.change_C2.set(True)
             
        ''' add buttons for class specific manipulation (MNIST only) '''
        self.check1 = Checkbutton(self.labelframeChange , text="C1",variable=self.change_C1,
                                     onvalue=True, offvalue=False)
        self.check2 = Checkbutton(self.labelframeChange , text="C2",variable=self.change_C2,
                                     onvalue=True, offvalue=False)
        
        self.check1.place(x = 0, y = 5)
        self.check2.place(x = 0, y = 25)
        
        ''' dimensionality reduction option '''
        self.dimRed = tk.BooleanVar(self)
        self.dimRed.set(False)
        self.check3 = Checkbutton(self.labelframeChange , text="Reduce Dim ",variable=self.dimRed,
                                     onvalue=True, offvalue=False, bg=self.bgColor,fg=self.fgColor)
        self.check3.place(x = 0, y = 45)

        ''' add bars for data manipulation settings '''
        self.labelframeSettings = LabelFrame(self.master, text="Data visualization", height = 510, width = 810,bg=self.bgColor,
                                                fg=self.fgColor)
        self.labelframeSettings.place(x=0, y=0)
        
        ''' add button to create data '''
        self.nextWindow = Button(self, text='Next window', command=self.create_data,height = 5, width = 10,bg=self.bgColor,
                                                fg=self.fgColor)
        self.nextWindow.place(x = 450, y = 530)
        
        ''' availabe datasets - add new dataset name here '''
        DATASETS_OxData = [
            "MNIST"
            ]
        self.datasetName = StringVar(self)
        self.datasetName.set(DATASETS_OxData[0]) # default value
        
        ''' options menues for OxData '''
        self.optOxData = OptionMenu(self, self.datasetName, *DATASETS_OxData)
        #self.optOxData["label"] = "Image dataset"
        self.optOxData.place(x = 410, y = 0)
        
        ''' add labels to options menu '''
        self.optOxDataLabel = Label(self)        
        self.optOxDataLabel.configure(text = "OxData Dataset: " )
        self.optOxDataLabel.place(x = 320, y = 0)
        
        ''' Evaluation parameters '''
        self.labelframeEvalParams = LabelFrame(self.master, text="Evaluation parameters:", height = 200, width = 200)
        self.labelframeEvalParams.place(x=1000, y=180) 
        
        self.headIm = Label(self.labelframeEvalParams)
        self.headEEG = Label(self.labelframeEvalParams) 
        self.headIm.configure(text = "Image:")
        self.headIm.place(x = 90, y = 5)
        self.headEEG.configure(text = "EEG:")
        self.headEEG.place(x = 140, y = 5)
        
        ''' add labels for SNR values'''
        self.im_SNR_C1 = Label(self.labelframeEvalParams)
        self.im_SNR_C2 = Label(self.labelframeEvalParams)
        
        self.sample_SNR_C1 = Label(self.labelframeEvalParams)
        self.sample_SNR_C2 = Label(self.labelframeEvalParams)
             
        self.yCorr_C1 = Label(self.labelframeEvalParams)
        self.yCorr_C2 = Label(self.labelframeEvalParams)
        
        self.im_SNR_C1.configure(text = "im. SNR (C1):\t" + str(0) + "\t" + str(0))
        self.im_SNR_C1.place(x = 0, y = 30)
        self.im_SNR_C2.configure(text = "im. SNR (C2):\t" + str(0) + "\t" + str(0))
        self.im_SNR_C2.place(x = 0, y = 50)
        self.sample_SNR_C1.configure(text = "sample. SNR (C1):\t" + str(0) + "\t" + str(0))
        self.sample_SNR_C1.place(x = 0, y = 75)
        self.sample_SNR_C2.configure(text = "sample. SNR (C2):\t" + str(0) + "\t" + str(0))
        self.sample_SNR_C2.place(x = 0, y = 95)
        
        self.yCorr_C1.configure(text = "Y-Corr C1:\t" + str(0) + "\t" + str(0))
        self.yCorr_C1.place(x = 0, y = 120)
        self.yCorr_C2.configure(text = "Y-Corr C2:\t" + str(0) + "\t" + str(0))
        self.yCorr_C2.place(x = 0, y = 140)
        
        ''' second pannel - placeholder'''
        self.labelframeEvalParams2 = LabelFrame(self.master, text="Class separability:",height = 80, width = 200)
        self.labelframeEvalParams2.place(x=1000, y=370) 
        
        self.im_SNR_diff = Label(self.labelframeEvalParams2)
        self.sample_SNR_diff = Label(self.labelframeEvalParams2)  
        
        self.im_SNR_diff.configure(text = "diff. im. SNR :\t" + str(0) + "\t" + str(0))
        self.im_SNR_diff.place(x = 0, y = 5)
        self.sample_SNR_diff.configure(text = "diff. samp. SNR:\t" + str(0) + "\t" + str(0))
        self.sample_SNR_diff.place(x = 0, y = 25)
        
    ''' button callbacks '''
    def create_data(self):

        ''' update data transformations (automatically creates changed datasets)'''
        self.dataSettings = {}
        print(self.dataSettings)
        

        #self.dataset.updateDatasets(self.dataSettings, self.datasetOxName.get(),
        #                                     [self.change_C1.get(),self.change_C2.get()])
        
        ''' reset/create canvas '''
        if self.figureHandle == 0:
            #plt.ioff() # disable ineractive mode to surpress empty figure
            #self.figureHandle = plt.figure(facecolor='k')
            #self.figureHandle = matplotlib.figure.Figure()
            self.figureHandle = Figure(figsize=(7,5), dpi=100)
            self.axesHandle = self.figureHandle.add_subplot(111)
        else:
            #self.figureHandle.clear(True)
            pass
            #plt.clf()
            #matplotlib.figure.clf()
            #self.canvas.destroy()
        
        ''' reset/create canvas '''
        try: 
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError: 
            pass 
        
        self.canvas = FigureCanvasTkAgg(self.figureHandle, self.labelframeSettings)
        #self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.NONE, expand=False)
        #self.canvas.get_tk_widget().place(x=320, y=40)
        
        self.plotData()

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.RIGHT, fill=tk.NONE, expand=True)
        
        ''' update SNR estimation '''
        #im_oxygen_value = self.dataset.calculateOx()
        
        #self.im_Oxygen.configure(text = "Oxygen:\t" + str(round(im_oxygen_value,2)))

        #''' show dataset parameters '''
        #self.configureDatasetParameters() 

    # helper methods
    def plotData(self):

        # plt.rcParams.update({'font.size': 8})

        dataPointer = 0
        window = self.dataset.OxData.window
        numberOfSamples = self.dataset.OxData.nSamples
        Fs = self.dataset.OxData.Fs

        for dataPointer in range(0,numberOfSamples-window,floor(0.1*self.dataset.OxData.Fs)):

            # label figure
            xTickArray = np.arange(0,window+Fs,Fs)
            xTickLabels = np.flip(xTickArray/(Fs))
            self.axesHandle.set_xticks(xTickArray , minor=False)
            self.axesHandle.set_xticklabels(xTickLabels, fontdict=None, minor=False)

            self.axesHandle.set_xlabel('time relative to current measurement [s]')
            self.axesHandle.set_ylabel('amplitude')
            self.axesHandle.set_ylim((25000,40000))
            self.axesHandle.grid()

            # create line plot
            data = self.dataset.OxData.data['PLETH'][dataPointer:dataPointer+window]
            self.axesHandle.plot(np.arange(0,len(data)),data) #,cmap='viridis')
            self.canvas.draw()
            
            # refresh figure for "real-time" visualization 
            self.axesHandle.clear()
            self.canvas.flush_events()
            time.sleep(0.1)
        #return 0
        
    def calculateOx(self):
        return 85
            
def main():
    root = tk.Tk()
    root.geometry("1200x600")
    root.state('zoomed')
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()