# IVEEDRIS GUI library
# Name: gui

from core import *

# Global shutdown of the GUI
def shutdown():
    #updateMsgsTimer.cancel()
    s = getObjectSerial()
    s.close()
    win = getObjectGUI()
    win.destroy()
    setInitGUIFlag(False)

global GUISaved
# Function for saving GUI object in gui modules
def saveObjectGUI(guiwin):
    global GUISaved
    GUISaved = guiwin

# Function for getting GUI object from gui modules
def getObjectGUI():
    global GUISaved
    return GUISaved
    
# Console input messages
def consoleWriteLeft(*message, end = "\n", sep = " "):
    if getPrintOnConsoleFlag():
        text = ""
        for item in message:
            text += "{}".format(item)
            #text = text[2:-1]
            text += sep
        text = str(text).replace('\\x','')
        text += end
        now = datetime.now()
        time_stamp = now.strftime("S [%H:%M:%S]: ")
        win = getObjectGUI()
        win.console.insert("end",time_stamp,"left")
        win.console.insert("end",text,"left")
        win.console.see(tk.END)
    
# Console output messages
def consoleWriteRight(*message, end = "\n", sep = " "):
    if getPrintOnConsoleFlag():
        text = ""
        for item in message:
            text += "{}".format(item)
            text += sep
        text += end
        now = datetime.now()
        time_stamp = now.strftime("M [%H:%M:%S]: ")
        win = getObjectGUI()
        win.console.insert("end",time_stamp,"right")
        win.console.insert("end",text,"right")
        win.console.see(tk.END)

# Send message button callback
def sendMessage():
    win = getObjectGUI()
    msgToSend = win.msg.get()
    consoleWriteRight(msgToSend)
    msgToSend = bytes.fromhex(msgToSend)
    s = getObjectSerial()
    s.write(msgToSend)

# Are you alive callback from buttom
def areYouAliveFromButton():
    consoleWriteRight(areYouAlive())

# Send Relay Configuration callback for Button:
def sendRelayConfigurationFromButton():
    setRelayConfigurationRdButtonSelected.set(None)
    stateRx = relayConfiguration.get()
    consoleWriteRight(sendRelayConfiguration(stateRx))
    
# Radio button for relay configuration send
def selectRelayConfigurationRadioButton():
    win = getObjectGUI()
    rC = win.setRelayConfigurationRdButtonSelected.get()
    if rC == 1:
        consoleWriteRight(sendIdleStateRelayConfiguration())
    elif rC == 2:
        consoleWriteRight(sendPotentiometryCalibrationStateRelayConfiguration())
    elif rC == 3:
        consoleWriteRight(sendDissolutionPotentiometryStateRelayConfiguration())
    elif rC == 4:
        consoleWriteRight(sendSubstratumPotentiometryStateRelayConfiguration())
    elif rC == 5:
        consoleWriteRight(sendVoltammetry2DissolutionStateRelayConfiguration())
    elif rC == 6:
        consoleWriteRight(sendVoltammetry2SubstratumStateStateRelayConfiguration())
    elif rC == 7:
        consoleWriteRight(sendVoltammetry3DissolutionStateRelayConfiguration())
    elif rC == 8:
        consoleWriteRight(sendVoltammetry3SubstratumStateRelayConfiguration())
    elif rC == 9:
        consoleWriteRight(sendGradientStateRelayConfiguration())
    elif rC == 10:
        consoleWriteRight(sendCurerntInjectionStateRelayConfiguration())
    elif rC == 11:
        consoleWriteRight(sendAllUpStateRelayConfiguration())
    elif rC == 12:
        consoleWriteRight(sendAllDownStateRelayConfiguration())    

# Current scale selection on radiobuttons callback
def selectCurrentScaleRadioButton():
    win = getObjectGUI()
    ss = win.setCurrentScaleRdButtonSelected.get()
    if ss == 1:
        consoleWriteRight(sendCurrentScale('0')) # Precision
    elif ss == 2:
        consoleWriteRight(sendCurrentScale('1')) # Large

# Send DAC Value callback from button
def sendDACValueFromButton():
    win = getObjectGUI()
    win.setTrue0VCheckButtonVar.set(0)
    dv = int(win.dacValue.get())
    consoleWriteRight(setDACValue(dv))
    consoleWriteRight(sendTrue0VCommand(0))
    
# Send True 0V command callback from checkbox
def sendTrue0VCommandCallbackOnButton():
    cmdSet = 0
    win = getObjectGUI()
    if win.setTrue0VCheckButtonVar.get()==1:
        cmdSet = 1
    consoleWriteRight(sendTrue0VCommand(cmdSet))

printTimeFlag = True

# Callback for checkbox off printing elapsed time per iteration
def printTimeCallback():
    cmdSet = 0
    win = getObjectGUI()
    if win.printTimeButtonVar.get()==1:
        cmdSet = 1
    setPrintTimeFlag(cmdSet)
    
# Setter for printTimeFlag
def setPrintTimeFlag(cmd):
    global printTimeFlag
    printTimeFlag = cmd
    
# Getter for printTimeFlag
def getPrintTimeFlag():
    global printTimeFlag
    return printTimeFlag 

# Checkbutton for plotting or not the communications in the console
def printOnConsoleCallback():
    cmdSet = 0
    win = getObjectGUI()
    if win.printOnConsoleCheckButtonVar.get()==1:
        cmdSet = 1
    setPrintOnConsoleFlag(cmdSet)

printOnConsoleFlag = True

# setter for printOnConsoleFlage
def setPrintOnConsoleFlag(cmd):
    global printOnConsoleFlag
    if cmd:
        printOnConsoleFlag = True
    else:
        printOnConsoleFlag = False

# getter for printOnConsoleFlag
def getPrintOnConsoleFlag():
    global printOnConsoleFlag
    return printOnConsoleFlag
    
# Ask ADCCM value callback from button
def askADCCMFromButton():
    consoleWriteRight(askADCValue('CM'))
    
# Ask ADCWE value callback from button
def askADCWEFromButton():
    consoleWriteRight(askADCValue('WE'))
    
# Ask ADCCE value callback from button
def askADCCEFromButton():
    consoleWriteRight(askADCValue('CE'))
    
# Ask ADCDAC value callback from button
def askADCDACFromButton():
    consoleWriteRight(askADCValue('DAC'))
    
# Send period from button from callback
def sendPeriodFromButton():
    consoleWriteRight(sendPeriod_A5incoming())
    
# Send wait period between waveform applications from button from callback
def sendWaitFromButton():
    consoleWriteRight(sendWait_A5incoming())
    
# Open file function for WV1
def openFileWV1():
    win = getObjectGUI()
    dir = filedialog.askopenfilename()
    win.WV1LoadPath.set(dir)
    
# Open file function for WV2
def openFileWV2():
    win = getObjectGUI()
    dir = filedialog.askopenfilename()
    win.WV2LoadPath.set(dir)
    
# Open file function for WV3
def openFileWV3():
    win = getObjectGUI()
    dir = filedialog.askopenfilename()
    win.WV3LoadPath.set(dir)
    
# Open file function for WV4
def openFileWV4():
    win = getObjectGUI()
    dir = filedialog.askopenfilename()
    win.WV4LoadPath.set(dir)
    
# Open file function for WV5
def openFileWV5():
    win = getObjectGUI()
    dir = filedialog.askopenfilename()
    win.WV5LoadPath.set(dir)
    
# Function for loading WV1 from file
def loadWV1FromFile():
    win = getObjectGUI()
    f = open(win.WV1LoadPath.get(),'r')
    WV1 = f.read()
    WV1 = [int(i) for i in WV1.split(';')]
    setWV(1,WV1)
    win.WV1LoadIndLabel.config(bg='deep sky blue')
    win.WV1LoadIndLabel2.config(bg='deep sky blue')
    f.close()
    
# Function for loading WV2 from file
def loadWV2FromFile():
    win = getObjectGUI()
    f = open(win.WV2LoadPath.get(),'r')
    WV2 = f.read()
    WV2 = [int(i) for i in WV2.split(';')]
    setWV(2,WV2)
    win.WV2LoadIndLabel.config(bg='deep sky blue')
    win.WV2LoadIndLabel2.config(bg='deep sky blue')
    f.close()
    
# Function for loading WV3 from file
def loadWV3FromFile():
    win = getObjectGUI()
    f = open(win.WV3LoadPath.get(),'r')
    WV3 = f.read()
    WV3 = [int(i) for i in WV3.split(';')]
    setWV(3,WV3)
    win.WV3LoadIndLabel.config(bg='deep sky blue')
    win.WV3LoadIndLabel2.config(bg='deep sky blue')
    f.close()
    
# Function for loading WV4 from file
def loadWV4FromFile():
    win = getObjectGUI()
    f = open(win.WV4LoadPath.get(),'r')
    WV4 = f.read()
    WV4 = [int(i) for i in WV4.split(';')]
    setWV(4,WV4)
    win.WV4LoadIndLabel.config(bg='deep sky blue')
    win.WV4LoadIndLabel2.config(bg='deep sky blue')
    f.close()
    
# Function for loading WV5 from file
def loadWV5FromFile():
    win = getObjectGUI()
    f = open(win.WV5LoadPath.get(),'r')
    WV5 = f.read()
    WV5 = [int(i) for i in WV5.split(';')]
    setWV(5,WV5)
    win.WV5LoadIndLabel.config(bg='deep sky blue')
    win.WV5LoadIndLabel2.config(bg='deep sky blue')
    f.close()

# Callback from button to send WV1 already loaded
def sendWV1FromButton():
    WV1 = getWV(1)
    consoleWriteRight(sendWV_A5incoming(WV1,1))

# Callback from button to send WV2 already loaded
def sendWV2FromButton():
    WV2 = getWV(2)
    consoleWriteRight(sendWV_A5incoming(WV2,2))
    
# Callback from button to send WV3 already loaded
def sendWV3FromButton():
    WV3 = getWV(3)
    consoleWriteRight(sendWV_A5incoming(WV3,3))
    
# Callback from button to send WV4 already loaded
def sendWV4FromButton():
    WV4 = getWV(4)
    consoleWriteRight(sendWV_A5incoming(WV4,4))
    
# Callback from button to send WV5 already loaded
def sendWV5FromButton():
    WV5 = getWV(5)
    consoleWriteRight(sendWV_A5incoming(WV5,5))

# Callback send application of WV n, N times
def sendApplyFromButton():
    win = getObjectGUI()
    try:
        openSaveFileGUI()
    except:
        now = datetime.now()
        win.savePath.set(os.getcwd()+'/'+now.strftime("%Y-%m-%d_%H-%M-%S")+'.ive')
        openSaveFileGUI()
    WVselected = int(win.selectWV.get())
    NOI = int(win.numberOfIterations.get())
    writeBeginSaveFile(WVselected,NOI)
    consoleWriteRight(sendApplyWaveform(WVselected, NOI))
    
# Callback for stop application
def sendStopFromButton():
    writeSaveFile('\n\n')
    consoleWriteRight(sendStop())
    
# Choose save path callback from button to find path /file
def chooseSaveFile():
    win = getObjectGUI()
    dir = filedialog.askopenfilename()
    win.savePath.set(dir)
    
# Function for opening file where save experiment data from GUI
def openSaveFileGUI():
    win = getObjectGUI()
    append = win.appendSave.get()
    if append:
        saveFile = open(win.savePath.get(),'a')
    else:
        saveFile = open(win.savePath.get(),'w')
    setSaveFile(saveFile)
        

### GUI INICIALIZATION ###
class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
       
        # GUI basics
        self.geometry("1000x600")
        self.title("IVEEDRIS-SCIR GUI")
        myFont=tkinter.font.Font(family='Helvetica',size=12)
        myBold=tkinter.font.Font(family='Helvetica',size=12, weight='bold')

        # Executes shutdown when close
        self.protocol("WM_DELETE_WINDOW", shutdown)

        # Header
        self.labelIntroduction = tk.Label(
            text="In Vitro Electrostimulation and Electrically-Controlled Drug Release Instrumentation System for Spinal Cord Injury Repair",
            font=myBold,
            fg="white",
            bg="SkyBlue4",
            width=112,
            height=1
        )
        self.labelIntroduction.place(x=0,y=0)

        # Console
        consoleHeight = 500
        self.consoleString = tk.StringVar()
        self.console = tk.Text(self,bg='white')
        self.console.tag_configure("right", justify="right")
        self.console.tag_configure("left", justify="left")
        self.console.place(x=10,y=30,width=385,height=consoleHeight)

        # Vertical column
        self.verticalColumnLabel = tk.Label(self, text=3, width=1, height=consoleHeight-70, bg="SkyBlue4")
        self.verticalColumnLabel.place(x=405,y=17)

        # Author label background
        self.horizontalSeparatorLabel = tk.Label(self, width=50, height=2, bg="SkyBlue4")
        self.horizontalSeparatorLabel.place(x=740,y=30*19)

        # Author label
        self.sendMessageLabel = tk.Label(self, text="Javier Monreal Trigo © 2021",font=myFont,height=1,fg='white',bg="SkyBlue4")
        self.sendMessageLabel.place(x=500+280,y=30+15+consoleHeight+30)

        # Send message string space
        self.sendMessageLabel = tk.Label(self, text="Message to send: ",font=myFont,height=1,fg='black')
        self.sendMessageLabel.place(x=10,y=30+10+consoleHeight)

        self.msg=tk.StringVar()
        self.messageToSendEntry=tk.Entry(self,textvariable=self.msg,width=20)
        self.messageToSendEntry.place(x=150,y=30+10+consoleHeight)

        # Send button
        self.sendButton=tk.Button(self,text='Send',font=myFont,command=sendMessage,
                             bg='SkyBlue3',height=1,width=4)
        self.sendButton.place(x=325,y=25+10+consoleHeight)

        # Ask if alive button
        self.aliveButton=tk.Button(self,text='Are you alive?',font=myFont,command=areYouAliveFromButton,
                             bg='SkyBlue3',height=1,width=12)
        self.aliveButton.place(x=325+75+25,y=30)

        # Relay set configuration
        self.sendRelayConfigurationLabel = tk.Label(self, text="Relay configuration: ",font=myFont,height=1,fg='black')
        self.sendRelayConfigurationLabel.place(x=325+75+25,y=30+40)

        self.relayConfiguration=tk.StringVar()
        self.relayConfigurationToSendEntry=tk.Entry(self,textvariable=self.relayConfiguration,width=10)
        self.relayConfigurationToSendEntry.place(x=325+75+150+15,y=30+40)

        # Send relay configuration button
        self.sendRelayConfigurationButton=tk.Button(self,text='Send',font=myFont,command=sendRelayConfigurationFromButton,
                             bg='SkyBlue3',height=1,width=4)
        self.sendRelayConfigurationButton.place(x=325+75+150+90+15,y=30+35)

        # Radio button for relay configuration send
        self.setRelayConfigurationRdButtonSelected = tk.IntVar() # Como StringVar pero en entero

        self.setRelayConfigurationRadioButton1 = tk.Radiobutton(self, text="Idle State", font=myFont, variable=self.setRelayConfigurationRdButtonSelected, 
                    value=1, command=selectRelayConfigurationRadioButton)
        self.setRelayConfigurationRadioButton1.place(x=400+25,y=100)
        self.setRelayConfigurationRadioButton2 = tk.Radiobutton(self, text="Potentiometry Calibration", font=myFont, variable=self.setRelayConfigurationRdButtonSelected,
                    value=2, command=selectRelayConfigurationRadioButton)
        self.setRelayConfigurationRadioButton2.place(x=400+25,y=100+20)
        self.setRelayConfigurationRadioButton3 = tk.Radiobutton(self, text="Dissolution Potentiometry", font=myFont, variable=self.setRelayConfigurationRdButtonSelected, 
                    value=3, command=selectRelayConfigurationRadioButton)
        self.setRelayConfigurationRadioButton3.place(x=400+25,y=100+20*2)
        self.setRelayConfigurationRadioButton4 = tk.Radiobutton(self, text="Substratum Potentiometry", font=myFont, variable=self.setRelayConfigurationRdButtonSelected, 
                    value=4, command=selectRelayConfigurationRadioButton)
        self.setRelayConfigurationRadioButton4.place(x=400+25,y=100+20*3)
        self.setRelayConfigurationRadioButton5 = tk.Radiobutton(self, text="2-e Dissolution Voltammetry", font=myFont, variable=self.setRelayConfigurationRdButtonSelected,
                    value=5, command=selectRelayConfigurationRadioButton)
        self.setRelayConfigurationRadioButton5.place(x=400+25,y=100+20*4)
        self.setRelayConfigurationRadioButton6 = tk.Radiobutton(self, text="2-e Substratum Voltammetry", font=myFont, variable=self.setRelayConfigurationRdButtonSelected, 
                    value=6, command=selectRelayConfigurationRadioButton)
        self.setRelayConfigurationRadioButton6.place(x=400+25,y=100+20*5)
        self.setRelayConfigurationRadioButton7 = tk.Radiobutton(self, text="3-e Dissolution Voltammetry", font=myFont, variable=self.setRelayConfigurationRdButtonSelected,
                    value=7, command=selectRelayConfigurationRadioButton)
        self.setRelayConfigurationRadioButton7.place(x=400+25,y=100+20*6)
        self.setRelayConfigurationRadioButton8 = tk.Radiobutton(self, text="3-e Substratum Voltammetry", font=myFont, variable=self.setRelayConfigurationRdButtonSelected, 
                    value=8, command=selectRelayConfigurationRadioButton)
        self.setRelayConfigurationRadioButton8.place(x=400+25,y=100+20*7)
        self.setRelayConfigurationRadioButton9 = tk.Radiobutton(self, text="Voltage Gradient", font=myFont, variable=self.setRelayConfigurationRdButtonSelected, 
                    value=9, command=selectRelayConfigurationRadioButton)
        self.setRelayConfigurationRadioButton9.place(x=400+25,y=100+20*8)
        self.setRelayConfigurationRadioButton10 = tk.Radiobutton(self, text="Current Injection", font=myFont, variable=self.setRelayConfigurationRdButtonSelected,
                    value=10, command=selectRelayConfigurationRadioButton)
        self.setRelayConfigurationRadioButton10.place(x=400+25,y=100+20*9)
        self.setRelayConfigurationRadioButton11 = tk.Radiobutton(self, text="All Up", font=myFont, variable=self.setRelayConfigurationRdButtonSelected, 
                    value=11, command=selectRelayConfigurationRadioButton)
        self.setRelayConfigurationRadioButton11.place(x=400+25,y=100+20*10)
        self.setRelayConfigurationRadioButton12 = tk.Radiobutton(self, text="All Down", font=myFont, variable=self.setRelayConfigurationRdButtonSelected,
                    value=12, command=selectRelayConfigurationRadioButton)
        self.setRelayConfigurationRadioButton12.place(x=400+25,y=100+20*11)

        # Set precision or large scale for current measurement radio button
        self.currentScaleLabel = tk.Label(self, text="Current Scale:",font=myFont,height=1,fg='black')
        self.currentScaleLabel.place(x=400+25,y=100+20*13)

        self.setCurrentScaleRdButtonSelected = tk.IntVar() # Como StrinVar pero en entero

        self.setCurrentScaleRadioButton1 = tk.Radiobutton(self, text="Precision Scale", font=myFont, variable=self.setCurrentScaleRdButtonSelected, 
                    value=1, command=selectCurrentScaleRadioButton)
        self.setCurrentScaleRadioButton1.place(x=400+25,y=100+20*14)
        self.setCurrentScaleRadioButton2 = tk.Radiobutton(self, text="Large Scale", font=myFont, variable=self.setCurrentScaleRdButtonSelected,
                    value=2, command=selectCurrentScaleRadioButton)
        self.setCurrentScaleRadioButton2.place(x=400+25,y=100+20*15)

        # Vertical column
        self.verticalColumnLabel2 = tk.Label(self, text=3, width=1, height=consoleHeight-70, bg="SkyBlue4")
        self.verticalColumnLabel2.place(x=400+330,y=17)

        # Set DAC Value
        self.setDACValueLabel = tk.Label(self, text="DAC Value to set:",font=myFont,height=1,fg='black')
        self.setDACValueLabel.place(x=400+25,y=100+20*17)

        self.dacValue=tk.StringVar()
        self.dacVAlueEntry=tk.Entry(self,textvariable=self.dacValue,width=10)
        self.dacVAlueEntry.place(x=325+75+150+10,y=100+20*17)

        # Send DAC value button
        self.sendDACValueButton=tk.Button(self,text='Send',font=myFont,command=sendDACValueFromButton,
                             bg='SkyBlue3',height=1,width=4)
        self.sendDACValueButton.place(x=325+75+150+90+10,y=95+20*17)

        # Set true 0V checkbutton
        self.setTrue0VCheckButtonVar=tk.IntVar()
        self.setTrue0VCheckButton=tk.Checkbutton(self, text='Set true 0V', font = myFont, variable=self.setTrue0VCheckButtonVar, onvalue=1, offvalue=0, command=sendTrue0VCommandCallbackOnButton)
        self.setTrue0VCheckButton.place(x=400+25,y=100+20*18)

        # Read ADCs values
        self.readADCCMValueButton=tk.Button(self,text='Ask CM',font=myFont,command=askADCCMFromButton,
                             bg='SkyBlue3',height=1,width=5)
        self.readADCCMValueButton.place(x=400+25,y=100+20*20)

        self.readADCCEValueButton=tk.Button(self,text='Ask CE',font=myFont,command=askADCCEFromButton,
                             bg='SkyBlue3',height=1,width=5)
        self.readADCCEValueButton.place(x=400+25+75,y=100+20*20)

        self.readADCWEValueButton=tk.Button(self,text='Ask WE',font=myFont,command=askADCWEFromButton,
                             bg='SkyBlue3',height=1,width=5)
        self.readADCWEValueButton.place(x=400+25+75*2,y=100+20*20)

        self.readADCDACValueButton=tk.Button(self,text='Ask DAC',font=myFont,command=askADCDACFromButton,
                             bg='SkyBlue3',height=1,width=5)
        self.readADCDACValueButton.place(x=400+25+75*3,y=100+20*20)

        self.ADCCMLabel = tk.Label(self, text="CM:",font=myFont,height=1,fg='black')
        self.ADCCMLabel.place(x=400+25,y=100+20*22)

        self.ADCDACLabel = tk.Label(self, text="DAC:",font=myFont,height=1,fg='black')
        self.ADCDACLabel.place(x=400+25,y=100+20*23)

        self.ADCWELabel = tk.Label(self, text="WE:",font=myFont,height=1,fg='black')
        self.ADCWELabel.place(x=400+25+125,y=100+20*22)

        self.ADCCELabel = tk.Label(self, text="CE:",font=myFont,height=1,fg='black')
        self.ADCCELabel.place(x=400+25+125,y=100+20*23)

        self.ADCCMValueLabelText = tk.StringVar()
        #self.ADCCMValueLabelText.set('0000')
        self.ADCCMValueLabel = tk.Label(self, textvariable=self.ADCCMValueLabelText,font=myFont,height=1,fg='black')
        self.ADCCMValueLabel.place(x=400+25+50,y=100+20*22)

        self.ADCDACValueLabelText = tk.StringVar()
        #self.ADCDACValueLabelText.set('0000')
        self.ADCDACValueLabel = tk.Label(self, textvariable=self.ADCDACValueLabelText,font=myFont,height=1,fg='black')
        self.ADCDACValueLabel.place(x=400+25+50,y=100+20*23)

        self.ADCWEValueLabelText = tk.StringVar()
        #self.ADCWEValueLabelText.set('0000')
        self.ADCWEValueLabel = tk.Label(self, textvariable=self.ADCWEValueLabelText,font=myFont,height=1,fg='black')
        self.ADCWEValueLabel.place(x=400+25+125+40,y=100+20*22)

        self.ADCCEValueLabelText = tk.StringVar()
        #self.ADCCEValueLabelText.set('0000')
        self.ADCCEValueLabel = tk.Label(self, textvariable=self.ADCCEValueLabelText,font=myFont,height=1,fg='black')
        self.ADCCEValueLabel.place(x=400+25+125+40,y=100+20*23)

        # WV1 load file
        self.WV1LoadLabel = tk.Label(self, text="WV1: ",font=myFont,height=1,fg='black')
        self.WV1LoadLabel.place(x=750,y=30+5)

        self.WV1LoadPath=tk.StringVar()
        self.WV1LoadPathEntry=tk.Entry(self,textvariable=self.WV1LoadPath,width=18)
        self.WV1LoadPathEntry.place(x=750+45,y=30+5)

        self.findPathWV1Button=tk.Button(self,text='/',font=myFont,command=openFileWV1,
                             bg='SkyBlue3',height=1,width=1)
        self.findPathWV1Button.place(x=750+201,y=30)

        loadWV1Button=tk.Button(self,text='Load',font=myFont,command=loadWV1FromFile,
                             bg='SkyBlue3',height=1,width=4)
        loadWV1Button.place(x=750,y=30+30)

        self.sendWV1Button=tk.Button(self,text='Send',font=myFont,command=sendWV1FromButton,
                             bg='SkyBlue3',height=1,width=4)
        self.sendWV1Button.place(x=750+100,y=30+30)

        self.WV1LoadIndLabel = tk.Label(self,height=1,bg='navy',width=3)
        self.WV1LoadIndLabel.place(x=750+69,y=30+5+27)
        self.WV1LoadIndLabel2 = tk.Label(self,height=1,bg='navy',width=3)
        self.WV1LoadIndLabel2.place(x=750+69,y=30+5+37)

        self.WV1SendIndLabel = tk.Label(self,height=1,bg='navy',width=3)
        self.WV1SendIndLabel.place(x=750+69+99,y=30+5+27)
        self.WV1SendIndLabel2 = tk.Label(self,height=1,bg='navy',width=3)
        self.WV1SendIndLabel2.place(x=750+69+99,y=30+5+37)

        # WV2 load file
        self.WV2LoadLabel = tk.Label(self, text="WV2: ",font=myFont,height=1,fg='black')
        self.WV2LoadLabel.place(x=750,y=30+5+30*2)

        self.WV2LoadPath=tk.StringVar()
        self.WV2LoadPathEntry=tk.Entry(self,textvariable=self.WV2LoadPath,width=18)
        self.WV2LoadPathEntry.place(x=750+45,y=30+5+30*2)

        self.findPathWV2Button=tk.Button(self,text='/',font=myFont,command=openFileWV2,
                             bg='SkyBlue3',height=1,width=1)
        self.findPathWV2Button.place(x=750+201,y=30+30*2)

        self.loadWV2Button=tk.Button(self,text='Load',font=myFont,command=loadWV2FromFile,
                             bg='SkyBlue3',height=1,width=4)
        self.loadWV2Button.place(x=750,y=30+30*2+30)

        self.sendWV2Button=tk.Button(self,text='Send',font=myFont,command=sendWV2FromButton,
                             bg='SkyBlue3',height=1,width=4)
        self.sendWV2Button.place(x=750+100,y=30+30*2+30)

        self.WV2LoadIndLabel = tk.Label(self,height=1,bg='navy',width=3)
        self.WV2LoadIndLabel.place(x=750+69,y=30+5+30*2+27)
        self.WV2LoadIndLabel2 = tk.Label(self,height=1,bg='navy',width=3)
        self.WV2LoadIndLabel2.place(x=750+69,y=30+5+30*2+37)

        self.WV2SendIndLabel = tk.Label(self,height=1,bg='navy',width=3)
        self.WV2SendIndLabel.place(x=750+69+99,y=30+5+30*2+27)
        self.WV2SendIndLabel2 = tk.Label(self,height=1,bg='navy',width=3)
        self.WV2SendIndLabel2.place(x=750+69+99,y=30+5+30*2+37)

        # WV3 load file
        self.WV3LoadLabel = tk.Label(self, text="WV3: ",font=myFont,height=1,fg='black')
        self.WV3LoadLabel.place(x=750,y=30+5+30*4)

        self.WV3LoadPath=tk.StringVar()
        self.WV3LoadPathEntry=tk.Entry(self,textvariable=self.WV3LoadPath,width=18)
        self.WV3LoadPathEntry.place(x=750+45,y=30+5+30*4)

        self.findPathWV3Button=tk.Button(self,text='/',font=myFont,command=openFileWV3,
                             bg='SkyBlue3',height=1,width=1)
        self.findPathWV3Button.place(x=750+201,y=30+30*4)

        self.loadWV3Button=tk.Button(self,text='Load',font=myFont,command=loadWV3FromFile,
                             bg='SkyBlue3',height=1,width=4)
        self.loadWV3Button.place(x=750,y=30+30*4+30)

        self.sendWV3Button=tk.Button(self,text='Send',font=myFont,command=sendWV3FromButton,
                             bg='SkyBlue3',height=1,width=4)
        self.sendWV3Button.place(x=750+100,y=30+30*4+30)

        self.WV3LoadIndLabel = tk.Label(self,height=1,bg='navy',width=3)
        self.WV3LoadIndLabel.place(x=750+69,y=30+5+30*4+27)
        self.WV3LoadIndLabel2 = tk.Label(self,height=1,bg='navy',width=3)
        self.WV3LoadIndLabel2.place(x=750+69,y=30+5+30*4+37)

        self.WV3SendIndLabel = tk.Label(self,height=1,bg='navy',width=3)
        self.WV3SendIndLabel.place(x=750+69+99,y=30+5+30*4+27)
        self.WV3SendIndLabel2 = tk.Label(self,height=1,bg='navy',width=3)
        self.WV3SendIndLabel2.place(x=750+69+99,y=30+5+30*4+37)

        # WV4 load file
        self.WV4LoadLabel = tk.Label(self, text="WV4: ",font=myFont,height=1,fg='black')
        self.WV4LoadLabel.place(x=750,y=30+5+30*6)

        self.WV4LoadPath=tk.StringVar()
        self.WV4LoadPathEntry=tk.Entry(self,textvariable=self.WV4LoadPath,width=18)
        self.WV4LoadPathEntry.place(x=750+45,y=30+5+30*6)

        self.findPathWV4Button=tk.Button(self,text='/',font=myFont,command=openFileWV4,
                             bg='SkyBlue3',height=1,width=1)
        self.findPathWV4Button.place(x=750+201,y=30+30*6)

        self.loadWV4Button=tk.Button(self,text='Load',font=myFont,command=loadWV4FromFile,
                             bg='SkyBlue3',height=1,width=4)
        self.loadWV4Button.place(x=750,y=30+30*6+30)

        self.sendWV4Button=tk.Button(self,text='Send',font=myFont,command=sendWV4FromButton,
                             bg='SkyBlue3',height=1,width=4)
        self.sendWV4Button.place(x=750+100,y=30+30*6+30)

        self.WV4LoadIndLabel = tk.Label(self,height=1,bg='navy',width=3)
        self.WV4LoadIndLabel.place(x=750+69,y=30+5+30*6+27)
        self.WV4LoadIndLabel2 = tk.Label(self,height=1,bg='navy',width=3)
        self.WV4LoadIndLabel2.place(x=750+69,y=30+5+30*6+37)

        self.WV4SendIndLabel = tk.Label(self,height=1,bg='navy',width=3)
        self.WV4SendIndLabel.place(x=750+69+99,y=30+5+30*6+27)
        self.WV4SendIndLabel2 = tk.Label(self,height=1,bg='navy',width=3)
        self.WV4SendIndLabel2.place(x=750+69+99,y=30+5+30*6+37)

        # WV5 load file
        self.WV5LoadLabel = tk.Label(self, text="WV5: ",font=myFont,height=1,fg='black')
        self.WV5LoadLabel.place(x=750,y=30+5+30*8)

        self.WV5LoadPath=tk.StringVar()
        self.WV5LoadPathEntry=tk.Entry(self,textvariable=self.WV5LoadPath,width=18)
        self.WV5LoadPathEntry.place(x=750+45,y=30+5+30*8)

        self.findPathWV5Button=tk.Button(self,text='/',font=myFont,command=openFileWV5,
                             bg='SkyBlue3',height=1,width=1)
        self.findPathWV5Button.place(x=750+201,y=30+30*8)

        self.loadWV5Button=tk.Button(self,text='Load',font=myFont,command=loadWV5FromFile,
                             bg='SkyBlue3',height=1,width=4)
        self.loadWV5Button.place(x=750,y=30+30*8+30)

        self.sendWV5Button=tk.Button(self,text='Send',font=myFont,command=sendWV5FromButton,
                             bg='SkyBlue3',height=1,width=4)
        self.sendWV5Button.place(x=750+100,y=30+30*8+30)

        self.WV5LoadIndLabel = tk.Label(self,height=1,bg='navy',width=3)
        self.WV5LoadIndLabel.place(x=750+69,y=30+5+30*8+27)
        self.WV5LoadIndLabel2 = tk.Label(self,height=1,bg='navy',width=3)
        self.WV5LoadIndLabel2.place(x=750+69,y=30+5+30*8+37)

        self.WV5SendIndLabel = tk.Label(self,height=1,bg='navy',width=3)
        self.WV5SendIndLabel.place(x=750+69+99,y=30+5+30*8+27)
        self.WV5SendIndLabel2 = tk.Label(self,height=1,bg='navy',width=3)
        self.WV5SendIndLabel2.place(x=750+69+99,y=30+5+30*8+37)

        # Horizontal separator
        self.horizontalSeparatorLabel = tk.Label(self, width=50, height=1, bg="SkyBlue4")
        self.horizontalSeparatorLabel.place(x=740,y=30*11+10)

        # Set period timer
        self.PeriodLabel = tk.Label(self, text="Period (us): ",font=myFont,height=1,fg='black')
        self.PeriodLabel.place(x=750,y=30*12+10)

        self.PeriodToSend = tk.StringVar()
        self.PeriodToSendEntry=tk.Entry(self,textvariable=self.PeriodToSend,width=10)
        self.PeriodToSendEntry.place(x=750+85,y=30*12+10)

        self.sendPeriodButton=tk.Button(self,text='Send',font=myFont,command=sendPeriodFromButton,
                             bg='SkyBlue3',height=1,width=4)
        self.sendPeriodButton.place(x=750+85+90,y=30*12+5)

        # Wait time between repatitions timer
        self.WaitLabel = tk.Label(self, text="Wait (us): ",font=myFont,height=1,fg='black')
        self.WaitLabel.place(x=750,y=30*13+10)

        self.WaitToSend=tk.StringVar()
        self.WaitToSendEntry=tk.Entry(self,textvariable=self.WaitToSend,width=10)
        self.WaitToSendEntry.place(x=750+85,y=30*13+10)

        self.sendWaitButton=tk.Button(self,text='Send',font=myFont,command=sendWaitFromButton,
                             bg='SkyBlue3',height=1,width=4)
        self.sendWaitButton.place(x=750+85+90,y=30*13+5)

        # Application of waveform
        self.applicationLabel = tk.Label(self, text="Application: ",font=myBold,height=1,fg='black')
        self.applicationLabel.place(x=750,y=30*14+10)

        self.applicationLabelWV = tk.Label(self, text="WV:",font=myFont,height=1,fg='black')
        self.applicationLabelWV.place(x=750,y=30*15+10)

        self.selectWV=tk.StringVar()
        self.selectWVEntry=tk.Entry(self,textvariable=self.selectWV,width=2)
        self.selectWVEntry.place(x=750+40,y=30*15+10)

        self.applicationLabelIter = tk.Label(self, text="Iterations:",font=myFont,height=1,fg='black')
        self.applicationLabelIter.place(x=750+70,y=30*15+10)

        self.numberOfIterations=tk.StringVar()
        self.numberOfIterationsEntry=tk.Entry(self,textvariable=self.numberOfIterations,width=11)
        self.numberOfIterationsEntry.place(x=750+145,y=30*15+10)

        self.sendApplyButton=tk.Button(self,text='Send',font=myFont,command=sendApplyFromButton,
                             bg='SkyBlue3',height=1,width=4)
        self.sendApplyButton.place(x=750,y=30*16+5)

        self.sendStopButton=tk.Button(self,text='STOP',font=myBold,command=sendStopFromButton,
                             bg='brown4',height=1,width=4)
        self.sendStopButton.place(x=750+85+90,y=30*16+5)

        self.saveLabel = tk.Label(self, text="Save: ",font=myFont,height=1,fg='black')
        self.saveLabel.place(x=750,y=30*18)

        self.savePath=tk.StringVar()
        self.savePathEntry=tk.Entry(self,textvariable=self.savePath,width=18)
        self.savePathEntry.place(x=750+45,y=30*18)

        self.savePathButton=tk.Button(self,text='/',font=myFont,command=chooseSaveFile,
                             bg='SkyBlue3',height=1,width=1)
        self.savePathButton.place(x=750+201,y=30*17+25)

        # Append to selected file checkbutton
        self.appendSave=tk.IntVar()
        self.appendSave.set(1)
        self.appendSaveCheckButton=tk.Checkbutton(self, text='Append results to existing', font = myFont, variable=self.appendSave, onvalue=1, offvalue=0)
        self.appendSaveCheckButton.place(x=750,y=30*17+8)
        
        # Set new messages on console checkbutton
        self.printOnConsoleCheckButtonVar=tk.IntVar()
        self.printOnConsoleCheckButton=tk.Checkbutton(self, text='Print on console', font = myFont, variable=self.printOnConsoleCheckButtonVar, onvalue=1, offvalue=0, command=printOnConsoleCallback)
        self.printOnConsoleCheckButton.place(x=10,y=210+20*18)
        self.printOnConsoleCheckButtonVar.set(1)
        setPrintOnConsoleFlag(1)
        
        # Set new messages on console checkbutton
        self.printTimeButtonVar=tk.IntVar()
        self.printTimeButton=tk.Checkbutton(self, text='Time elapsed on shell', font = myFont, variable=self.printTimeButtonVar, onvalue=1, offvalue=0, command=printTimeCallback)
        self.printTimeButton.place(x=160,y=210+20*18)
        self.printTimeButtonVar.set(0)
        setPrintTimeFlag(0)
        
        # Say to global environament that the GUI is online
        setInitGUIFlag(True)
        
