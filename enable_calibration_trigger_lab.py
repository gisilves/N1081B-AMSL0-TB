import sys
import time
import os.path
import socket
from send_mail import *
from datetime import datetime
from N1081B_sdk import N1081B
#from client_charge_tagger_L0BT_20231022 import *

ipdevice1 = "caenplu-perugia1.cern.ch"
ipdevice2 = "caenplu-perugia2.cern.ch"

def disable_master_trigger():
    N1081B_device1.configure_digital_generator(N1081B.Section.SEC_C,False,False,False,False)

def enable_calibration():
    N1081B_device1.configure_digital_generator(N1081B.Section.SEC_C,True,True,True,True)
    N1081B_device1.configure_pulse_generator(N1081B.Section.SEC_B,
                                        N1081B.StatisticMode.STAT_DETERMINISTIC,
                                        250, 1000000, True, True, True, True)

def disable_pulser():
    N1081B_device1.configure_pulse_generator(N1081B.Section.SEC_B,
                                             N1081B.StatisticMode.STAT_DETERMINISTIC,
                                             250, 100000000, False, False, False, False)

def reset_scalers():
    N1081B_device2.reset_channel(N1081B.Section.SEC_D,0,N1081B.FunctionType.FN_SCALER)
    N1081B_device2.reset_channel(N1081B.Section.SEC_D,1,N1081B.FunctionType.FN_SCALER)
    N1081B_device2.reset_channel(N1081B.Section.SEC_D,2,N1081B.FunctionType.FN_SCALER)
    N1081B_device2.reset_channel(N1081B.Section.SEC_D,3,N1081B.FunctionType.FN_SCALER)

    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tScalers reset before calibration trigger")

if __name__ == "__main__":

    N1081B_device1 = N1081B(ipdevice1)
    N1081B_device2 = N1081B(ipdevice2)

    msg1 = ""
    msg2 = ""
    msg3 = ""

    goodconnection1 = False;
    goodconnection2 = False;

while goodconnection1==False or goodconnection2==False: 
    try:
        N1081B_device1.connect()
    except:
        now = datetime.now()
        print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tNo connection for device 1 (" + ipdevice1 + ")")
        msg1 += now.strftime("%d/%m/%Y %H:%M:%S")
        msg1 += "\n\n"
        msg1 += "No connection for device 1 ("
        msg1 += ipdevice1
        msg1 += ")\n\n"
        #    send_mail(msg1)
    else:
        goodconnection1 = True
    finally:
        pass

    try:
        N1081B_device2.connect()
    except:
        now = datetime.now()
        print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tNo connection for device 2 (" + ipdevice2 + ")")
        msg2 += now.strftime("%d/%m/%Y %H:%M:%S")
        msg2 += "\n\n"
        msg2 += "No connection for device 2 ("
        msg2 += ipdevice2
        msg2 += ")\n\n"
        #    send_mail(msg2)
    else:
        goodconnection2 = True
    finally:
        pass
            
    if (goodconnection1 == True and goodconnection2 == True):

        if (msg1 != "" or msg2 != ""): 
            msgtosend = socket.gethostname() + "/" + os.path.basename(__file__) + "\n\n"
            now = datetime.now()
            msgtosend += now.strftime("%d/%m/%Y %H:%M:%S")
            msgtosend += "\n\nfinally the connection to both boards is ok, but we had:\n\n"
            msgtosend += msg1 + msg2
            send_mail(msgtosend)
       
        # login with password
        authorized1 = N1081B_device1.login("12345")
        authorized2 = N1081B_device2.login("12345")

        if (authorized1 and authorized2):
            disable_pulser()
            
            #    send_run_cmd("STOP", 0, "/Data/BLOCKS/USBLF_PCGSC03/", "/home/ams/lontra/log.txt")
            
            N1081B_device1.start_acquisition(N1081B.Section.SEC_D, N1081B.FunctionType.FN_LUT)
            
            now = datetime.now()
            print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tStarting CAL trigger ...")
            
            disable_master_trigger()
            
            now = datetime.now()
            print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tAll triggers disabled")
            
            reset_scalers()
            
            #    send_run_cmd("START", 0, "/Data/BLOCKS/USBLF_PCGSC03/", "/home/ams/lontra/log.txt")
            
            enable_calibration()
            
            now = datetime.now()
            print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tCAL triggers enabled")
                        
            # close connection
            N1081B_device1.disconnect()
            N1081B_device2.disconnect()
        else:
            now = datetime.now()
            print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tWrong password")
            msg3 += socket.gethostname() + "/" + os.path.basename(__file__) + "\n\n"
            msg3 += now.strftime("%d/%m/%Y %H:%M:%S")
            msg3 += "\n\n"
            msg3 += "Wrong password"
            msg3 += "\n\n"
            send_mail(msg3)
            
        break

    else:
        msgtosend = socket.gethostname() + "/" + os.path.basename(__file__) + "\n\n"
        msgtosend += msg1 + msg2
        send_mail(msgtosend)

    time.sleep(60) 
