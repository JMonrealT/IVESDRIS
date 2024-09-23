# IVEEDRIS template for spectific applications
# Name: APP (can be modified)

from core import *

screamerIfNotImplemented = False # can be changed 
verbose = False # can be changed
global saving
saving = True # can be changed

def sNewMsg(inputMessage):
    if verbose:
        print(inputMessage) # By default terminal shows messages received if flag activated
    if inputMessage.find('ee0000ee') !=-1:
        print('END RECEIVED ee0000ee!')
    
def sDDmessageRx(processMsg):
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sDDmessageRx be implemented!') # Complete here!

def sADCDACRx(value):
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sADCDACRxTo be implemented!') # Complete here!
    
def sADCWERx(value):
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sADCWERx To be implemented!') # Complete here!
    
def sADCCERx(value):
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sADCCERx To be implemented!') # Complete here!
    
def sADCCMRx(value):
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sADCCMRx To be implemented!') # Complete here!
    
def sPeriodSentA5Rx():#(value):
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sPeriodSentA5Rx To be implemented!') # Complete here!
    
def sWaitSentA5Rx():
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sWaitSentA5Rx To be implemented!') # Complete here!
    
def sPeriodSentRx():
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sPeriodSentRx To be implemented!') # Complete here!
    
def sWaitSentRx():
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sWaitSentRx To be implemented!') # Complete here!
    
def sWV1SentA5Rx():
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sWV1SentA5Rx To be implemented!') # Complete here!

def sWV2SentA5Rx():
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sWV2SentA5Rx To be implemented!') # Complete here!

def sWV3SentA5Rx():
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sWV3SentA5Rx To be implemented!') # Complete here!

def sWV4SentA5Rx():
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sWV4SentA5Rx To be implemented!') # Complete here!

def sWV5SentA5Rx():
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sWV5SentA5Rx To be implemented!') # Complete here!
        
def sWV1SentRx():
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sWV1SentRx To be implemented!') # Complete here!

def sWV2SentRx():
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sWV2SentRx To be implemented!') # Complete here!

def sWV3SentRx():
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sWV3SentRx To be implemented!') # Complete here!

def sWV4SentRx():
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sWV4SentRx To be implemented!') # Complete here!

def sWV5SentRx():
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        print('sWV5SentRx To be implemented!') # Complete here!
        
def sNOISentA5Rx():
    global sendNOIFlag
    if screamerIfNotImplemented:
        print('sNOISentA5Rx To be implemented!') # Complete here!
        
def sMSMRx(value):
    global screamerIfNotImplemented
    if screamerIfNotImplemented:
        selectCommunication('IVEEDRIS')
        time.sleep(0.01)
        setMSMessageSentFlag(False)
        if value == 'aa':
            1+1 # Correct, complete here!
        else:
            1+1 # An error ocurred, complete here!
        print('sMSMRx To be implemented!') # Complete here!
