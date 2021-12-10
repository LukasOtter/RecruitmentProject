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
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

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
        menu = Menu(self.master)
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
        self.initializePannel()
            
        ''' create default datsets (first array entry) '''
        self.datasetOxData = Dataset(self.datasetOxData.get(),'EEGNet')
        #self.datasetEEG = Dataset(self.datasetEEGName.get(),'EEGNet')
        #exit()
  
    def initializePannel(self): 
        
        ''' add labels for dataset settings'''
        
        self.labelframeC1 = LabelFrame(self.master, text="Settings C1", height = 95, width = 200)
        self.labelframeC2 = LabelFrame(self.master, text="Settings C2", height = 95, width = 200)
        self.labelframeC1.place(x = 540, y = 525)
        self.labelframeC2.place(x = 760, y = 525)

        self.signalLabelC1 = Label(self.labelframeC1,text = "Signal: " + str(100))        
        self.dataSizeLabelC1 = Label(self.labelframeC1,text = "Datasize: " + str(500))      
        self.linNoiseLabelC1 = Label(self.labelframeC1,text = "Lin. Noise: " + str(0))    
        self.corrNoiseLabelC1 = Label(self.labelframeC1,text = "Corr. Noise: " + str(0))
        self.xShiftLabelC1 = Label(self.labelframeC1,text = "X-Shift: " + str(0))
        self.yShiftLabelC1 = Label(self.labelframeC1,text = "nShuffle: " + str(0))
        
        self.signalLabelC1.place(x = 0, y = 5)
        self.dataSizeLabelC1.place(x = 100, y = 5)
        self.linNoiseLabelC1.place(x = 0, y = 25)   
        self.corrNoiseLabelC1.place(x = 100, y = 25)
        self.xShiftLabelC1.place(x = 0, y = 45)
        self.yShiftLabelC1.place(x = 100, y = 45)
        
        self.signalLabelC2 = Label(self.labelframeC2,text = "Signal: " + str(100))        
        self.dataSizeLabelC2 = Label(self.labelframeC2,text = "Datasize: " + str(500))      
        self.linNoiseLabelC2 = Label(self.labelframeC2,text = "Lin. Noise: " + str(0))    
        self.corrNoiseLabelC2 = Label(self.labelframeC2,text = "Corr. Noise: " + str(0))
        self.xShiftLabelC2 = Label(self.labelframeC2,text = "X-Shift: " + str(0))
        self.yShiftLabelC2 = Label(self.labelframeC2,text = "nShuffle: " + str(0))
        
        self.signalLabelC2.place(x = 0, y = 5)
        self.dataSizeLabelC2.place(x = 100, y = 5)
        self.linNoiseLabelC2.place(x = 0, y = 25)   
        self.corrNoiseLabelC2.place(x = 100, y = 25)
        self.xShiftLabelC2.place(x = 0, y = 45)
        self.yShiftLabelC2.place(x = 100, y = 45)
               
        ''' add bool for class-specific manipulations '''
        self.labelframeChange = LabelFrame(self.master, text="MNIST:", height = 95, width = 120)
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
                                     onvalue=True, offvalue=False)
        self.check3.place(x = 0, y = 45)

        ''' add bars for data manipulation settings '''
        self.labelframeSettings = LabelFrame(self.master, text="Manipulation parameters", height = 410, width = 310)
        self.labelframeSettings.place(x=0, y=0)
        self.w2 = Scale(self.labelframeSettings, from_=0, to=1200, length=300,tickinterval=150, orient=HORIZONTAL)
        self.w2["label"] = "X-shift [ms]"
        self.w2.set(0)
        self.w2.place(x=0, y=10)
        # self.w2.pack()
        self.w3 = Scale(self.labelframeSettings, from_=0, to=64, length=300,tickinterval=8, orient=HORIZONTAL)
        self.w3["label"] = "nShuffle [channels]"
        self.w3.set(0)
        self.w3.place(x=0, y=85)
        #self.w3.pack()
        self.w4 = Scale(self.labelframeSettings, from_=0, to=1000, length=300,tickinterval=100,orient=HORIZONTAL)
        self.w4["label"] = "signal [%]"
        self.w4.set(100)
        self.w4.place(x=0, y=160)
        self.w5 = Scale(self.labelframeSettings, from_=0, to=1000, length=300,tickinterval=100,orient=HORIZONTAL)
        self.w5["label"] = "constant noise [%]"
        self.w5.set(0)
        self.w5.place(x=0, y=235)
        self.w6 = Scale(self.labelframeSettings, from_=0, to=1000, length=300,tickinterval=100,orient=HORIZONTAL)
        self.w6["label"] = "correlated noise [%]"
        self.w6.set(0)
        self.w6.place(x=0, y=310)
        
        ''' add bars for data size settings '''
        self.labelframeDataSizeSettings = LabelFrame(self.master, text="Data size parameters", height = 190, width = 310)
        self.labelframeDataSizeSettings.place(x=0, y=430)   
        self.w7 = Scale(self.labelframeDataSizeSettings, from_=50, to=3000, length=300,tickinterval=500,orient=HORIZONTAL)
        self.w7["label"] = "data size"
        self.w7.set(500)
        self.w7.place(x=0, y=0)
        
        self.w8 = Scale(self.labelframeDataSizeSettings, from_=0, to=100, length=300,tickinterval=10,orient=HORIZONTAL)
        self.w8["label"] = "class balance"
        self.w8.set(50)
        self.w8.place(x=0, y=75)
        
        ''' add button to create data '''
        self.createData = Button(self, text='Create data', command=self.create_data,height = 5, width = 10)
        self.createData.place(x = 450, y = 530)
        
        ''' availabe datasets - add new dataset name here '''
        DATASETS_OxData = [
            "MNIST"
            ]
        self.datasetOxDataName = StringVar(self)
        self.datasetOxDataName.set(DATASETS_OxData[0]) # default value
        
        ''' options menues for OxData '''
        self.optOxData = OptionMenu(self, self.datasetOxData, *DATASETS_OxData)
        #self.optOxData["label"] = "Image dataset"
        self.optOxData.place(x = 410, y = 0)
        
        ''' add labels to options menu '''
        self.optOxDataLabel = Label(self)        
        self.optOxDataLabel.configure(text = "OxData Dataset: " )
        self.optOxDataLabel.place(x = 320, y = 0)
        
        
        ''' add buttons for shift analysis '''
        self.shiftEEG = Button(self, text='Analyze\ntemporal\nshift\n(EEG)', command=self.shift_analysis_EEG,height = 6, width = 10)
        self.shiftEEG.place(x = 1000, y = 50)
        
        self.shiftImage = Button(self, text='Analyze\ntemporal\nshift\n(Image)', command=self.shift_analysis_Image,height = 6, width = 10)
        self.shiftImage.place(x = 1090, y = 50)
        
        ''' add buttons for shift analysis '''
        self.rankData = Button(self, text='Rank\nsynthetic\ndataset\n', command=self.rank_Dataset,height = 6, width = 10)
        self.rankData.place(x = 1180, y = 50)
        
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
        self.dataSettings = {'X-shift': self.w2.get(), 
                             'nShuffle': self.w3.get(), 'signal': self.w4.get(),
                             'lin. Noise': self.w5.get(),'corr. Noise': self.w6.get(),
                             'dataSize': self.w7.get(),'class ratio': self.w8.get()/100,
                             'dimRed': self.dimRed.get()}
        print(self.dataSettings)
        

        self.datasetImage.updateDatasets(self.dataSettings, self.datasetImageName.get(),
                                              [self.change_C1.get(),self.change_C2.get()])
        
        ''' reset/create canvas '''
        if self.figureHandle == 0:
            plt.ioff() # disable ineractive mode to surpress empty figure
            self.figureHandle = plt.figure(facecolor="white")
        else:
            #.figureHandle.clear(True)
            plt.clf()
            #self.canvas.destroy()
        
        ''' reset/create canvas '''
        try: 
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError: 
            pass 
        
        self.canvas = FigureCanvasTkAgg(self.figureHandle, self)
        self.canvas.draw()
        #self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.NONE, expand=False) 
        self.canvas.get_tk_widget().place(x=320, y=40)
        
        self.datasetOxData.plotData(self.figureHandle)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.RIGHT, fill=tk.NONE, expand=True)
        
        ''' update SNR estimation '''
        im_oxygen_value = self.datasetOxData.calculateOX()
        
        self.im_Oxygen.configure(text = "Oxygen:\t" + str(round(im_oxygen_value,2)))

        ''' show dataset parameters '''
        self.configureDatasetParameters()
 
    def configureDatasetParameters(self):
        ''' update dataset paramater pannel values '''
        dataSettingsOxData = self.datasetOxData.returnDataSettings('C1')

        
    def popup_bonus(self):
        self.pop_up = tk.Toplevel()
        self.pop_up.wm_title("Results")
        self.pop_up.geometry("640x485")
        
        # ''' button to close pop up '''
        # b = Button(self.pop_up, text="Okay", command=self.pop_up.destroy)
        # b.grid(row=1, column=0)
        
        ''' canvas for plot '''
        canvas = FigureCanvasTkAgg(self.figureHandle, self.pop_up)
        canvas.draw()
        #self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.NONE, expand=False) 
        canvas.get_tk_widget().place(x=0, y=0)
            
def main():
    root = tk.Tk()
    root.geometry("1200x600")
    root.state('zoomed')
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()