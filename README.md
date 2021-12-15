# RecruitmentProject

Application allows the visualization of the pleth, hearthrate and functional blood oxygen saturation of arterial hemoglobin (%SpO2). The metrics are recovered from data returned by the OEM III Pulse Oximetry Module from Nonin. It is read from a binary .dat file and decoded from the deveoper's data format #7 (see datasheets in "UserGuides" folder for details on the binary encoding).


Run *./Application.py* script to start the GUI.
Press _Scan data_ button to scan the file in the data folder.

Required packages: _Python 3.-, Tkinter, Matplotlib, Numpy_


Sample GUI putput:

![Alt text](examples/sampleGUIoutput.jpg?raw=true "GUI")


