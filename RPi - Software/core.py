# IVEEDRIS system core library
# Name: core

### LIBRARIES ###

import tkinter as tk
from tkinter import filedialog
import tkinter.font
import serial
import time
import threading
import codecs
from datetime import datetime
import numpy as np
import os
import math
import RPi.GPIO as gpio

## HW SETUP

# Hardware init function
def hwInit():
    # Configure GPIO for controlling both UART-RS interfaces
    # RE_M! 11 | GPIO 0          |
    # RE_S! 13 | GPIO 2          |
    # DE_M  15 | GPIO 3   GPIO 4 | 16 DE_S
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD) 
    gpio.setup(11, gpio.OUT)
    gpio.output(11, True)
    gpio.setup(13, gpio.OUT)
    gpio.output(13, False)
    gpio.setup(15, gpio.OUT)
    gpio.output(15, False)
    gpio.setup(16, gpio.OUT)
    gpio.output(16, True)

    # Serial init
    s = serial.Serial('/dev/serial0',1843200)#921600)
    saveObjectSerial(s)
    
# Select communication between IVEEDRIS and MS
def selectCommunication(dest): # dest = ('IVEEDRIS','MS')
    # Configure GPIO for controlling both UART-RS interfaces
    # RE_M! 11 | GPIO 0          |
    # RE_S! 13 | GPIO 2          |
    # DE_M  15 | GPIO 3   GPIO 4 | 16 DE_S
    s = getObjectSerial()
    if dest == 'IVEEDRIS':
        s.baudrate = 1843200
        gpio.output(11, True)
        gpio.output(13, False)
        gpio.output(15, False)
        gpio.output(16, True)
    else:
        s.baudrate = 115200
        gpio.output(11, False)
        gpio.output(13, True)
        gpio.output(15, True)
        gpio.output(16, False)

# PRINCIPAL GETTERS AND SETTERS
	
# Function for saving serial object in core modules
def saveObjectSerial(serial):
    global serialSaved
    serialSaved = serial

# Function for getting serial object from core modules
def getObjectSerial():
    global serialSaved
    return serialSaved

global initGUIFlag
initGUIFlag = False

# Function for saving serial object in core modules
def setInitGUIFlag(flag):
    global initGUIFlag
    initGUIFlag = flag

# Function for getting serial object from core modules
def getInitGUIFlag():
    global initGUIFlag
    return initGUIFlag
	
## FUNCTION SPACE
        
# Calculate checksum function
def calculateChecksum(strHex):
    CMDbytes = 0
    for i in range(0,len(strHex)//2):
        CMDbytes += int(strHex[(i*2):(i*2+2)],16)
    CMDbytes = hex(CMDbytes%256)[2:]
    while(len(CMDbytes)<2):
        CMDbytes = '0'+CMDbytes
    return(CMDbytes)

# Are you alive callback (sends message):
def areYouAlive():
    msgToSend = "acc000"
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    s = getObjectSerial()
    s.write(msgToSendbytes)
    return msgToSend

# Send end of experiment ack:
def sendEndOfExperimentAck():
    msgToSend = "ee0000"
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    s = getObjectSerial()
    s.write(msgToSendbytes)
    return msgToSend

# Send Relay Configuration callback:
def sendRelayConfiguration(state):
    lastSendRelayConfiguration = state
    setLastSendRelayConfiguration(lastSendRelayConfiguration)
    CMDbytes = getCMDForRelayConfiguration(state)
    msgToSend = 'ac'+CMDbytes
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    s = getObjectSerial()
    s.write(msgToSendbytes)
    return msgToSend
    
# Secondary function for getting CMD + info por relay configuration
def getCMDForRelayConfiguration(state):
    cmdBytes = hex(int('000000'+state, 2))[2:]
    while(len(cmdBytes)<4):
        cmdBytes = '0'+cmdBytes
    return cmdBytes

# 1 Send Idle State Relay Configuration Callback
def sendIdleStateRelayConfiguration():
    return sendRelayConfiguration(IdleState)

# 2 Send Potentiometry Calibration State Relay Configuration Callback
def sendPotentiometryCalibrationStateRelayConfiguration():
    return sendRelayConfiguration(potentiometryCalibrationState)

# 3 Send Potentiometry Dissolution State Relay Configuration Callback
def sendDissolutionPotentiometryStateRelayConfiguration():
    return sendRelayConfiguration(PotentiometryDissolutionState)

# 4 Send Potentiometry Substratum State Relay Configuration Callback
def sendSubstratumPotentiometryStateRelayConfiguration():
    return sendRelayConfiguration(PotentiometrySubstratumState)

# 5 Send Voltammetry 2 Dissolution State Relay Configuration Callback
def sendVoltammetry2DissolutionStateRelayConfiguration():
    return sendRelayConfiguration(Voltammetry2DissolutionState)

# 6 Send Voltammetry 2 Substratum State Relay Configuration Callback
def sendVoltammetry2SubstratumStateStateRelayConfiguration():
    return sendRelayConfiguration(Voltammetry2SubstratumState)

# 7 Send Voltammetry 3 Dissolution State Relay Configuration Callback
def sendVoltammetry3DissolutionStateRelayConfiguration():
    return sendRelayConfiguration(Voltammetry3DissolutionState)
    
# 8 Send Voltammetry 3 Substratum State Relay Configuration Callback
def sendVoltammetry3SubstratumStateRelayConfiguration():
    return sendRelayConfiguration(Voltammetry3SubstratumState)

# 9 Send Gradient State Relay Configuration Callback
def sendGradientStateRelayConfiguration():
    return sendRelayConfiguration(GradientState)

# 10 Send Current Injection State Relay Configuration Callback
def sendCurerntInjectionStateRelayConfiguration():
    return sendRelayConfiguration(CurrentInjectionState)
    
# 11 Send All Up State Relay Configuration Callback
def sendAllUpStateRelayConfiguration():
    return sendRelayConfiguration(allUpState)
    
# 12 Send All Down State Relay Configuration Callback
def sendAllDownStateRelayConfiguration():
    return sendRelayConfiguration(allDownState)
   
# Send Current Scale Configuration:
def sendCurrentScale(scale):
    lastSendIscale = scale
    setLastSendIscale(lastSendIscale)
    bs = '00100000'+'0000000'+scale
    cmdBytes = hex(int(bs, 2))[2:]
    while(len(cmdBytes)<4):
        cmdBytes = '0'+cmdBytes
    msgToSend = 'ac'+cmdBytes
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    s = getObjectSerial()
    s.write(msgToSendbytes)
    return msgToSend
    
# Send DAC Value 
def setDACValue(value): #str from 0 to 4095
    cmdBytes = hex(int(value)+2**14)[2:] #+2**14 == |0b0100 0000 0x00
    while(len(cmdBytes)<4):
        cmdBytes = '0'+cmdBytes
    msgToSend = 'ac'+cmdBytes
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    s = getObjectSerial()
    s.write(msgToSendbytes)

# Send True 0V command
def sendTrue0VCommand(cmd):
    lastSendTrue0V = str(cmd)
    setLastSendTrue0V(lastSendTrue0V)
    highB111 = 2**15+2**14+2**13 # 0b1110 0x000
    cmdBytes = hex(highB111+cmd)[2:] 
    while(len(cmdBytes)<4):
        cmdBytes = '0'+cmdBytes
    msgToSend = 'ac'+cmdBytes
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    s = getObjectSerial()
    s.write(msgToSendbytes)
    return msgToSend
    
# Ask ADC value function
def askADCValue(adcSelect):
    highB011 = 2**14+2**13 # 0b0110 0x000
    if adcSelect == 'CM':
        cmd = 0
    elif adcSelect == 'CE':
        cmd = 1
    elif adcSelect == 'WE':
        cmd = 2
    elif adcSelect == 'DAC':
        cmd = 3
    cmdBytes = hex(highB011+cmd)[2:] 
    while(len(cmdBytes)<4):
        cmdBytes = '0'+cmdBytes
    msgToSend = 'ac'+cmdBytes
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    s = getObjectSerial()
    s.write(msgToSendbytes)
    return msgToSend

# Send NOI function A5 sending for extension (comming 4 data bytes)
def sendNOI_A5incoming():
    msgToSend = 'a50004'
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    setSendNOIFlag(True)
    s = getObjectSerial()
    s.write(msgToSendbytes)
    return msgToSend

# Send NOI function
def sendNOI(noi):
    msgToSend = 'a611'
    lastSendNOI = str(noi)
    setLastSendNOI(lastSendNOI)
    byte=hex(noi)[2:]
    while(len(byte)<8):
        byte = '0'+byte
    msgToSend += byte
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    s = getObjectSerial()
    s.write(msgToSendbytes)
    return msgToSend

# Send period function A5 sending for extension (comming 4 data bytes)
def sendPeriod_A5incoming():
    msgToSend = 'a50004'
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    setSendPeriodFlag(True)
    s = getObjectSerial()
    s.write(msgToSendbytes)
    return msgToSend

# Send period function
def sendPeriod(period):
    msgToSend = 'a677'
    lastSendPeriod = str(period)
    setLastSendPeriod(lastSendPeriod)
    byte=hex(period)[2:]
    while(len(byte)<8):
        byte = '0'+byte
    msgToSend += byte
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    s = getObjectSerial()
    s.write(msgToSendbytes)
    return msgToSend
    
# Send wait function A5 sending for extension (comming 4 data bytes)
def sendWait_A5incoming():
    msgToSend = 'a50004'
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    sendWaitFlag = True
    setSendWaitFlag(sendWaitFlag)
    s = getObjectSerial()
    s.write(msgToSendbytes)
    return msgToSend

# Send wait function
def sendWait(period):
    lastSendWait = str(period)
    setLastSendWait(lastSendWait)
    msgToSend = 'a675'
    byte=hex(period)[2:]
    while(len(byte)<8):
        byte = '0'+byte
    msgToSend += byte
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    s = getObjectSerial()
    s.write(msgToSendbytes)
    return msgToSend

# Send waveform slot (1 to 5) function A5 sending for extension (comming 4 data bytes)
def sendWV_A5incoming(vector,slot):
    msgToSend = 'a5'
    N1N2=hex(len(vector)*2)[2:]
    while(len(N1N2)<4):
        N1N2 = '0'+N1N2
    msgToSend += N1N2
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    sendWV1Flag = getSendWVFlag(1)
    sendWV2Flag = getSendWVFlag(2)
    sendWV3Flag = getSendWVFlag(3)
    sendWV4Flag = getSendWVFlag(4)
    sendWV5Flag = getSendWVFlag(5)
    if slot == 1:
        setSendWVFlag(1,True)
    elif slot == 2:
        setSendWVFlag(2,True)
    elif slot == 3:
        setSendWVFlag(3,True)
    elif slot == 4:
        setSendWVFlag(4,True)
    elif slot == 5:
        setSendWVFlag(5,True)
    s = getObjectSerial()
    s.write(msgToSendbytes)
    return msgToSend

# Function for sending WV 1 to 5
def sendWV(vector,slot):
    msgToSend = 'a65'+str(slot)
    hexstr = ''
    for i in range(len(vector)):
        twoBytes=hex(vector[i])[2:]
        while(len(twoBytes)<4):
            twoBytes = '0'+twoBytes
        hexstr += twoBytes
    msgToSend += hexstr
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    s = getObjectSerial()
    s.write(msgToSendbytes)
    return msgToSend

# Function for apply n WV, N times
def sendApplyWaveform(wv, times):
    generateTrue0Vvector(wv)
    msgToSend = 'ac'
    twoBytes = 2**15+2**13+(2**10)*wv+times
    twoBytes = hex(twoBytes)[2:]
    while(len(twoBytes)<4):
        twoBytes = '0'+twoBytes
    msgToSend += twoBytes
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    s = getObjectSerial()
    s.write(msgToSendbytes)
    return msgToSend
    
true0Vvector = [0,0,0,0,0]
true0Vvector_index = 0

# Function to obtain a True0V vector
def generateTrue0Vvector(wv):
    global true0Vvector, true0Vvector_index
    true0Vvector_index = 0
    wv = getWV(wv)
    true0Vvector = [0 for i in range(len(wv))]
    for i in range(len(wv)):
        if wv[i] == 4096:
            true0Vvector[i] = 1
            
# Function to obtain the values of the true0Vvector
def getTrue0Vvector():
    global true0Vvector
    return true0Vvector

# Function to get true0Vvector_index value
def getTrue0Vvector_index():
    global true0Vvector_index
    return true0Vvector_index

# Function to add one to lobal true0Vvector_index
def add1toTrue0Vvector_index():
    global true0Vvector_index, true0Vvector
    true0Vvector_index = true0Vvector_index + 1
    if true0Vvector_index >= len(true0Vvector):
        true0Vvector_index = 0
    
# Function for sending Stop command
def sendStop():
    msgToSend = 'ac'
    oneByte = 2**15
    oneByte = hex(oneByte)[2:]
    while(len(oneByte)<4):
        oneByte = '0'+oneByte
    msgToSend += oneByte
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    s = getObjectSerial()
    s.write(msgToSendbytes)
    return msgToSend

# Function for loading waveform inside variable space WV
def loadWV(wv,dir):
    f = open(dir,'r')
    WV = f.read()
    WV = [int(i) for i in WV.split(';')]
    setWV(wv,WV)
    f.close()
    
# Function for opening file where save experiment data
def openSaveFile(dir,append):
    if append:
        saveFile = open(dir,'a')
    else:
        saveFile = open(dir,'w')
    setSaveFile(saveFile)
        
# Function for closing saveFlie
def closeSaveFile():
    saveFile = getSaveFile()
    try:
        saveFile.close()
    except:
        print('Exception on close save file')
        
# Function for writing in saveFile
def writeSaveFile(msg):
    saveFile = getSaveFile()
    try:
        saveFile.write(msg)
    except:
        print('Exception on write in file, not open, trying to write: '+msg)

# Function for writing the begining of experiment in saveFile
def writeBeginSaveFile(WVselected,NOI):
    now = datetime.now()
    time_stamp = now.strftime("%H:%M:%S, on %d-%m-%Y")
    writeSaveFile('Experience started at ' + time_stamp + '\n')
    writeSaveFile('Waveform applied ' + str(WVselected) + ':\n')
    WV1 = getWV(1)
    WV2 = getWV(2)
    WV3 = getWV(3)
    WV4 = getWV(4)
    WV5 = getWV(5)
    if WVselected == 1:
        writeSaveFile(str(WV1)[1:-1].replace(', ',';')+'\n')
        setsizeOfWv(len(WV1))
    elif WVselected == 2:
        writeSaveFile(str(WV2)[1:-1].replace(', ',';')+'\n')
        setsizeOfWv(len(WV2))
    elif WVselected == 3:
        writeSaveFile(str(WV3)[1:-1].replace(', ',';')+'\n')
        setsizeOfWv(len(WV3))
    elif WVselected == 4:
        writeSaveFile(str(WV4)[1:-1].replace(', ',';')+'\n')
        setsizeOfWv(len(WV4))
    elif WVselected == 5:
        writeSaveFile(str(WV5)[1:-1].replace(', ',';')+'\n')
        setsizeOfWv(len(WV5))
    lastSendRelayConfiguration = getLastSendRelayConfiguration()
    lastSendPeriod = getLastSendPeriod()
    lastSendWait = getLastSendWait()
    if NOI!=0:
        setLastSendNOI(NOI)
    lastSendNOI = getLastSendNOI()
    writeSaveFile('Waveform applied ' + str(lastSendNOI) + ' times\n')
    writeSaveFile('Relay configuration: ' + lastSendRelayConfiguration + '\n')
    writeSaveFile('Period (us): ' + lastSendPeriod + '\n')
    writeSaveFile('Wait between iterations (us): ' + lastSendWait + '\n')
    writeSaveFile('Time (us);True0;ADC_DAC;ADC_CM;ADC_CE;ADC_WE;Iscale;Relays'+'\n')
    wvs = np.zeros((0,4),dtype='int') #0 CM, 1 CE, 2 WE, 3 DAC
    setwvs(wvs)
    setTimeCount(0)
    setiter_cnt(0)
    setOngoingFlag(True)
    
# Function for setting MS in certain position
def setMSRelays(relayPosition): # relayPosition = '00' to '12'
    selectCommunication('MS')
    time.sleep(0.01)
    msgToSend = 'aa'+relayPosition+'00'
    msgToSend += calculateChecksum(msgToSend)
    msgToSendbytes = bytes.fromhex(msgToSend)
    s = getObjectSerial()
    s.write(msgToSendbytes)
    setMSMessageSentFlag(True)
    timer = threading.Timer(4, timeoutMS) # 4 seconds, changing relay positions (36) takes 3.6 seconds
    timer.start()
    return msgToSend

# Timeout function for MS ACK or Error
def timeoutMS():
    if getMSMessageSentFlag():
        print('Timeout achieved on MS wait for answer! - from core lib')
        setMSMessageSentFlag(False)
        selectCommunication('IVEEDRIS')
        time.sleep(0.01)
    

# VARIABLES SPACE, GETTERS AND SETTERS

MSDisconnect = '00'
MSPosition1 = '01'
MSPosition2 = '02'
MSPosition3 = '03'
MSPosition4 = '04'
MSPosition5 = '05'
MSPosition6 = '06'
MSPosition7 = '07'
MSPosition8 = '08'
MSPosition9 = '09'
MSPosition10 = '10'
MSPosition11 = '11'
MSPosition12 = '12'

IdleState = '0011110000'
GradientState = '1110111100'
PotentiometryDissolutionState = '0001000000'
PotentiometrySubstratumState = '1011000000'
Voltammetry3DissolutionState = '0000100000'
Voltammetry3SubstratumState = '1010100000'
Voltammetry2DissolutionState = '0000101000'
Voltammetry2SubstratumState = '1010101000'
CurrentInjectionState = '1111111111'
allUpState = '1111111111'
allDownState = '0000000000'
potentiometryCalibrationState = '1111000100'

lastSendRelayConfiguration = IdleState

# Function for getting last sent relay configuration
def getLastSendRelayConfiguration():
    global lastSendRelayConfiguration
    return lastSendRelayConfiguration

# Function for setting last sent relay configuration
def setLastSendRelayConfiguration(state):
    global lastSendRelayConfiguration
    lastSendRelayConfiguration = state
	
saveFile = ''

# Function for saving save file handler
def setSaveFile(file):
    global saveFile
    saveFile = file
  
# Function for saving getting file handler
def getSaveFile():
    global saveFile
    return saveFile

sizeOfWv = 0

# Function for getting size of waveform before start application
def getsizeOfWv():
    global sizeOfWv
    return sizeOfWv

# Function for saving size of waveform before start application
def setsizeOfWv(sz):
    global sizeOfWv
    sizeOfWv = sz

sendWV1Flag = False
sendWV2Flag = False
sendWV3Flag = False
sendWV4Flag = False
sendWV5Flag = False
WV1 = []
WV2 = []
WV3 = []
WV4 = []
WV5 = []

# Function for saving send waveform flag
def setSendWVFlag(wv,state):
    global sendWV1Flag
    global sendWV2Flag
    global sendWV3Flag
    global sendWV4Flag
    global sendWV5Flag
    if wv==1:
        sendWV1Flag = state
    elif wv==2:
        sendWV2Flag = state
    elif wv==3:
        sendWV3Flag = state
    elif wv==4:
        sendWV4Flag = state
    elif wv==5:
        sendWV5Flag = state
    
# Function for getting WVs in environment
def getWV(wv):
    global WV1
    global WV2
    global WV3
    global WV4
    global WV5
    if wv==1:
        return WV1 
    elif wv==2:
        return WV2 
    elif wv==3:
        return WV3 
    elif wv==4:
        return WV4 
    elif wv==5:
        return WV5 
    
# Function for saving WVs in environment
def setWV(wv,vector):
    global WV1
    global WV2
    global WV3
    global WV4
    global WV5
    if wv==1:
        WV1 = vector
    elif wv==2:
        WV2 = vector
    elif wv==3:
        WV3 = vector
    elif wv==4:
        WV4 = vector
    elif wv==5:
        WV5 = vector
    
# Function for getting WV send flags
def getSendWVFlag(wv):
    global sendWV1Flag
    global sendWV2Flag
    global sendWV3Flag
    global sendWV4Flag
    global sendWV5Flag
    if wv==1:
        return sendWV1Flag
    elif wv==2:
        return sendWV2Flag
    elif wv==3:
        return sendWV3Flag
    elif wv==4:
        return sendWV4Flag
    elif wv==5:
        return sendWV5Flag
		
# Function for saving lastSendWait 
def setLastSendWait(state):
    global lastSendWait 
    lastSendWait = state

lastSendWait = -1

# Function for getting lastSendWait 
def getLastSendWait():
    global lastSendWait 
    return lastSendWait 
	
# Function for saving lastSendPeriod 
def setLastSendPeriod(state):
    global lastSendPeriod 
    lastSendPeriod = state

lastSendPeriod = -1

# Function for getting lastSendPeriod 
def getLastSendPeriod ():
    global lastSendPeriod 
    return lastSendPeriod 
	
lastSendTrue0V = '0'

# Function for getting last sent True0V
def getLastSendTrue0V():
    global lastSendTrue0V
    return lastSendTrue0V

# Function for setting last sent True0V
def setLastSendTrue0V(state):
    global lastSendTrue0V
    lastSendTrue0V = state   
	
lastSendIscale = '0'

# Function for getting last sent current scale
def getLastSendIscale():
    global lastSendIscale
    return lastSendIscale

# Function for setting last sent current scale
def setLastSendIscale(state):
    global lastSendIscale
    lastSendIscale = state   	
	
sendPeriodFlag = False
# Function for saving sendPeriodFlag
def setSendPeriodFlag(state):
    global sendPeriodFlag
    sendPeriodFlag = state
    
# Function for getting sendPeriodFlag
def getSendPeriodFlag():
    global sendPeriodFlag
    return sendPeriodFlag
	
sendWaitFlag = False
# Function for saving sendWaitFlag
def setSendWaitFlag(state):
    global sendWaitFlag
    sendWaitFlag = state
    
# Function for getting sendWaitFlag
def getSendWaitFlag():
    global sendWaitFlag
    return sendWaitFlag

wvs = np.zeros((0,4),dtype='int') #0 CM, 1 CE, 2 WE, 3 DAC

# Function for setting wvs
def setwvs(in_wvs):
    global wvs
    wvs = in_wvs

# Function for getting wvs
def getwvs():
    global wvs
    return wvs

TimeCount = 0

# Function for setting TimeCount
def setTimeCount(n):
    global TimeCount
    TimeCount = n
    
# Function for getting TimeCount
def getTimeCount():
    global TimeCount
    return TimeCount 

iter_cnt = 0

# Function for setting iter_cnt
def setiter_cnt(n):
    global iter_cnt
    iter_cnt = n
    
# Function for getting iter_cnt
def getiter_cnt():
    global iter_cnt
    return iter_cnt

ongoingFlag = False

# Function for setting ongoingFlag
def setOngoingFlag(state):
    global ongoingFlag
    ongoingFlag = state
    
# Function for getting ongoingFlag
def getOngoingFlag():
    global ongoingFlag
    return ongoingFlag

sendNOIFlag = False

# Function for getting sendNOIFlag
def getSendNOIFlag():
    global sendNOIFlag
    return sendNOIFlag

# Function for setting sendNOIFlag
def setSendNOIFlag(cmd):
    global sendNOIFlag
    sendNOIFlag = cmd

lastSendNOI = -1

# Function for getting lastSendNOI
def getLastSendNOI():
    global lastSendNOI
    return lastSendNOI

# Function for setting lastSendNOI
def setLastSendNOI(n):
    global lastSendNOI
    lastSendNOI = n

MSMessageSentFlag = False

# Function for getting MSMessageSentFlag
def getMSMessageSentFlag():
    global MSMessageSentFlag
    return MSMessageSentFlag

# Function for setting MSMessageSentFlag
def setMSMessageSentFlag(n):
    global MSMessageSentFlag
    MSMessageSentFlag = n