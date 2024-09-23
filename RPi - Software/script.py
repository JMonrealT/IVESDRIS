# JAVIER MONREAL TRIGO
# 26th November 2022
# Description: BCEF configuration for specific experiment

ELECTROSTIMULATION = 3 # 1: ES+, 2: ES++, 3: ES-

from gui import *
from core import *
from com import *

GUIOn = False

hwInit() # Init hw (gpio & serial)

setPrintTimeFlag(0) # Prints time elapsed in console

s = getObjectSerial()
s.flushInput()

if GUIOn:
    win=GUI() # Init GUI
    saveObjectGUI(win) # Save GUI handle
updateMsgs() # Continuous thread start
if GUIOn:
    win.mainloop() # Infinite loop

if not GUIOn: # Script if GUI not started
    print("Preparing launch! ")
    step = 0.2 #s
    
    areYouAlive()
    time.sleep(step)
    
    sendIdleStateRelayConfiguration()
    time.sleep(step)
    
    sendCurrentScale('0') # Large
    time.sleep(step)
    
    sendTrue0VCommand(1)
    time.sleep(step)
    
    setDACValue(2048)
    time.sleep(step)
    
    askDirectory = False
    if askDirectory:
        root = tk.Tk()
        root.update()
        dir = filedialog.askopenfilename()
        root.destroy()
    else:
        if ELECTROSTIMULATION == 1:
            dir = '/home/pi/Desktop/1Dec2022 BCEF/ES+.iwv'
        elif ELECTROSTIMULATION == 2:
            dir = '/home/pi/Desktop/1Dec2022 BCEF/ES++.iwv'
        else:
            dir = '/home/pi/Desktop/1Dec2022 BCEF/ES-.iwv'
    
    loadWV(1,dir)
          
    sendWV_A5incoming(getWV(1),1)
    time.sleep(step)
    # A6 handled in app.py
    
    sendPeriod_A5incoming()
    time.sleep(step)    
    sendPeriod(100) #us
    time.sleep(step)
    
    sendWait_A5incoming()
    time.sleep(step)
    if ELECTROSTIMULATION == 1:
        sendWait(9700)
    elif ELECTROSTIMULATION == 2:
        sendWait(9700)
    else:
        sendWait(7900)
    time.sleep(step)
    
    sendNOI_A5incoming()
    time.sleep(step)
    #sendNOI(8640000) #24h
    #sendNOI(1440000) #4h
    #sendNOI(360000) #1h
    sendNOI(1000) #10sec
    time.sleep(step)
    
    print("Setting relay configuration! ")
    
    sendCurerntInjectionStateRelayConfiguration()
    time.sleep(1)
    
    dir = '/home/pi/Desktop/1Dec2022 BCEF/save.ive'
    openSaveFile(dir,0) # dir,append   
    
    WVselected = 1
    NOI = 0 # Number of iterations
    # if 0, it keeps the sent in the large mode, here just up to 1000
    writeBeginSaveFile(WVselected,NOI)
    
    sendTrue0VCommand(0)
    time.sleep(step)
    
    now = datetime.now()
    time_stamp = now.strftime("%H:%M:%S, on %d-%m-%Y")
    print('Start! '+time_stamp)
    
    sendApplyWaveform(WVselected, NOI) # WV, times
    
    cnt = 1
    tic = time.time()
    while getOngoingFlag():
        toc = time.time()
        if toc-tic>cnt:
            print('Started: '+time_stamp+' '+str(math.floor(cnt/3600))+'h, '+str(math.floor(cnt/60)-math.floor(cnt/3600)*60)+'m, '+str(cnt%60)+'s elapsed ')
            cnt+=1
    
    sendIdleStateRelayConfiguration()
    time.sleep(0.5)
    
    sendTrue0VCommand(1)
    time.sleep(step)
    
    setDACValue(2048)
    time.sleep(step)
    
    now = datetime.now()
    time_stamp = now.strftime("%H:%M:%S, on %d-%m-%Y")
    print('Finished! '+time_stamp)
    
t = getUpdateMsgsTimer()
t.cancel()
    
    
    
    

