# IVEEDRIS Communications methods
# Name: com

from core import *
from gui import *
from app import * # You can change the name of app for different specific scripts

global tic, toc, cnttictoc
tic = 0
toc = 0
cnttictoc = 1

global periodToCheckMsgs
periodToCheckMsgs = 0.01 # en segundos, 1ms
# Continuous thread every periodToCheckMsgs s
def updateMsgs():
    global expectingMsg, processMsg
    s = getObjectSerial()
    try:
        bytes_to_read = s.inWaiting()
    except:
        bytes_to_read = 0
    if expectingMsg & (bytes_to_read == 0):
        expectingMsg = False
        processMsg = ''
    if bytes_to_read > 0:
        inputMessage = s.read(bytes_to_read)
        inputMessage = inputMessage.hex()
        initGUIFlag = getInitGUIFlag()
        if initGUIFlag:
            consoleWriteLeft(inputMessage)
        else:
            sNewMsg(inputMessage)
        if getMSMessageSentFlag():
            processInputMSMessage(inputMessage)
        else:
            processInputMessage(inputMessage)
    global tic,toc,cnttictoc
    cnttictoc += 1
    if cnttictoc%9==0:
        tic = time.time()
    if cnttictoc%10==0: # 1 out of 10, it affects perfomanace
        toc = time.time()
        if getPrintTimeFlag():
            print(toc-tic,flush=True)
        cnttictoc = 1
    global updateMsgsTimer
    updateMsgsTimer = threading.Timer(periodToCheckMsgs, updateMsgs) 
    updateMsgsTimer.start()
    
processMsg = ''
expectingMsg = False

# Process input message function
def processInputMessage(msg):
    global processMsg, expectingMsg
    tzs = getTrue0Vvector()
    text = ""
    sep = " "
    for item in msg:
        text += "{}".format(item)
        text += sep
    text = str(text).replace('\\x','')
    
    initGUIFlag = getInitGUIFlag()
    if initGUIFlag:
        win = getObjectGUI()
    
    initLenProcessMsg = len(processMsg)
    if initLenProcessMsg>0 & expectingMsg:
        msg = processMsg + msg
        expectingMsg = False
    endOfMsg=len(msg)
    i=0
    messagesStill = True
    while messagesStill:
        global saving
        remainingMsg = msg[i:]
        head = remainingMsg[0:2]
        if head=='dd' and saving:
            if len(remainingMsg)>=20:
                processMsg = remainingMsg[0:20]
                i+=20
                value_cm=int(processMsg[2:6],16)
                value_ce=int(processMsg[6:10],16)
                value_we=int(processMsg[10:14],16)
                value_dac=int(processMsg[14:18],16)
                if not initGUIFlag:
                    sDDmessageRx(processMsg)
                lastSendRelayConfiguration = getLastSendRelayConfiguration()
                lastSendPeriod = getLastSendPeriod()
                lastSendWait = getLastSendWait()
                lastSendIscale = getLastSendIscale()
                
                lastSendTrue0V = tzs[getTrue0Vvector_index()]
                setLastSendTrue0V(lastSendTrue0V)
                add1toTrue0Vvector_index()
                
                TimeCount = getTimeCount()
                iter_cnt = getiter_cnt()
                sizeOfWv = getsizeOfWv()
                if iter_cnt!=0:
                    if iter_cnt%sizeOfWv==0:
                        if int(lastSendWait)!=0:
                            #TimeCount+=int(lastSendWait) 
                            TimeCount+=int(lastSendWait)+int(lastSendPeriod)
                        else:
                            TimeCount+=int(lastSendPeriod)
                    else:
                        TimeCount+=int(lastSendPeriod)
    
                iter_cnt+=1
                setiter_cnt(iter_cnt)
                setTimeCount(TimeCount)
                writeSaveFile(str(TimeCount)+';'+str(lastSendTrue0V)+';'+str(value_dac)+';'+str(value_cm)+';'+str(value_ce)+';'+str(value_we)+';'+lastSendIscale+';'+lastSendRelayConfiguration+'\n')
                #wvs=np.vstack((wvs,[value_cm,value_ce,value_we,value_dac])) #0 CM, 1 CE, 2 WE, 3 DAC
                processMsg = ''
                expectingMsg = False
            else:
                processMsg = remainingMsg
                expectingMsg = True
        else:
            if(len(remainingMsg)>=8):
                processMsg = remainingMsg[0:8]
                i+=8
                value = int(processMsg[2:6],16)
                if head=='a0': # 4B, CM incoming
                    if initGUIFlag:
                        win.ADCCMValueLabelText.set(str(value))
                    else:
                        sADCCMRx(value)
                elif head=='a1': # 4B, CE incoming
                    if initGUIFlag:
                        win.ADCCEValueLabelText.set(str(value))
                    else:
                        sADCCERx(value)
                elif head=='a2': # 4B, WE incoming
                    if initGUIFlag:
                        win.ADCWEValueLabelText.set(str(value))
                    else:
                        sADCWERx(value)
                elif head=='a3': # 4B, DAC incoming
                    if initGUIFlag:
                        win.ADCDACValueLabelText.set(str(value))
                    else:
                        sADCDACRx(value)
                elif head=='a5':
                    sendWV1Flag = getSendWVFlag(1)
                    sendWV2Flag = getSendWVFlag(2)
                    sendWV3Flag = getSendWVFlag(3)
                    sendWV4Flag = getSendWVFlag(4)
                    sendWV5Flag = getSendWVFlag(5)
                    sendPeriodFlag = getSendPeriodFlag()
                    sendWaitFlag = getSendWaitFlag()
                    sendNOIFlag = getSendNOIFlag()
                    if sendNOIFlag == True:
                        setSendNOIFlag(False)
                        if not initGUIFlag:
                            sNOISentA5Rx()
                    if sendPeriodFlag == True:
                        setSendPeriodFlag(False)
                        if initGUIFlag:
                            consoleWriteRight(sendPeriod(int(win.PeriodToSend.get())))
                        else:
                            sPeriodSentA5Rx()
                    elif sendWaitFlag == True:
                        setSendWaitFlag(False)
                        if initGUIFlag:
                            consoleWriteRight(sendWait(int(win.WaitToSend.get())))
                        else:
                            sWaitSentA5Rx()
                    elif sendWV1Flag == True:
                        WV1 = getWV(1)
                        if initGUIFlag:
                            consoleWriteRight(sendWV(WV1,1))
                        else:
                            sendWV(getWV(1),1)
                            sWV1SentA5Rx()
                    elif sendWV2Flag == True:
                        WV2 = getWV(2)
                        if initGUIFlag:
                            consoleWriteRight(sendWV(WV2,2))
                        else:
                            sendWV(getWV(2),2)
                            sWV2SentA5Rx()
                    elif sendWV3Flag == True:
                        WV3 = getWV(3)
                        if initGUIFlag:
                            consoleWriteRight(sendWV(WV3,3))
                        else:
                            sendWV(getWV(3),3)
                            sWV3SentA5Rx()
                    elif sendWV4Flag == True:
                        WV4 = getWV(4)
                        if initGUIFlag:
                            consoleWriteRight(sendWV(4,WV4))
                        else:
                            sendWV(getWV(4),4)
                            sWV4SentA5Rx()
                    elif sendWV5Flag == True:
                        WV5 = getWV(5)
                        if initGUIFlag:
                            consoleWriteRight(sendWV(WV5,5))
                        else:
                            sendWV(getWV(5),5)
                            sWV5SentA5Rx()
                elif head=='ee':
                    setOngoingFlag(False)
                    now = datetime.now()
                    if initGUIFlag:
                        consoleWriteRight(sendEndOfExperimentAck())
                    else:
                        sendEndOfExperimentAck()
                    time_stamp = now.strftime("%d/%m/%Y, %H:%M:%S")
                    writeSaveFile('\nEnd of stimulation '+ time_stamp +' \n\n\n')
                    closeSaveFile()
                elif head=='a6':
                    sendWV1Flag = getSendWVFlag(1)
                    sendWV2Flag = getSendWVFlag(2)
                    sendWV3Flag = getSendWVFlag(3)
                    sendWV4Flag = getSendWVFlag(4)
                    sendWV5Flag = getSendWVFlag(5)
                    if sendWV1Flag == True:
                        setSendWVFlag(1,False)
                        if initGUIFlag:                            
                            win.WV1SendIndLabel.config(bg='deep sky blue')
                            win.WV1SendIndLabel2.config(bg='deep sky blue')
                        else:
                            sWV1SentRx()
                    if sendWV2Flag == True:
                        setSendWVFlag(2,False)
                        if initGUIFlag:                            
                            win.WV2SendIndLabel.config(bg='deep sky blue')
                            win.WV2SendIndLabel2.config(bg='deep sky blue')
                        else:
                            sWV2SentRx()
                    if sendWV3Flag == True:
                        setSendWVFlag(3,False)
                        if initGUIFlag:                            
                            win.WV3SendIndLabel.config(bg='deep sky blue')
                            win.WV3SendIndLabel2.config(bg='deep sky blue')
                        else:
                            sWV3SentRx()
                    if sendWV4Flag == True:
                        setSendWVFlag(4,False)
                        if initGUIFlag:                            
                            win.WV4SendIndLabel.config(bg='deep sky blue')
                            win.WV4SendIndLabel2.config(bg='deep sky blue')
                        else:
                            sWV4SentRx()
                    if sendWV5Flag == True:
                        setSendWVFlag(5,False)
                        if initGUIFlag:                            
                            win.WV5SendIndLabel.config(bg='deep sky blue')
                            win.WV5SendIndLabel2.config(bg='deep sky blue')
                        else:
                            sWV5SentRx()
                processMsg = ''
                expectingMsg = False
            else:
                processMsg = remainingMsg
                expectingMsg = True
        if (i>=endOfMsg) | expectingMsg:
            messagesStill = False
            
# Process MS input message
def processInputMSMessage(msg):
    text = ""
    sep = " "
    for item in msg:
        text += "{}".format(item)
        text += sep
    text = str(text).replace('\\x','')
    
    initGUIFlag = getInitGUIFlag()
    if initGUIFlag:
        win = getObjectGUI()
    
    value = msg [0:2]
    sMSMRx(value)
            
# updateMsgsTimer getter
def getUpdateMsgsTimer():
    global updateMsgsTimer
    return updateMsgsTimer