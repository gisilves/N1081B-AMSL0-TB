import sys
from datetime import datetime
from N1081B_sdk import N1081B
#from client_charge_tagger_L0BT_20231022 import *

def disable_master_trigger():
    N1081B_device1.configure_digital_generator(N1081B.Section.SEC_C,False,False,False,False)

def enable_beam_trigger():
    N1081B_device1.configure_digital_generator(N1081B.Section.SEC_C,False,False,True,True)
#    N1081B_device1.configure_pulse_generator(N1081B.Section.SEC_B,
#                                             N1081B.StatisticMode.STAT_DETERMINISTIC,
#                                             250, 100000000, True, True, True, True)

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
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tScalers reset before DAQ trigger")

if __name__ == "__main__":
    N1081B_device1 = N1081B("caenplu-perugia1.cern.ch")
    N1081B_device1.connect()

    N1081B_device2 = N1081B("caenplu-perugia2.cern.ch")
    N1081B_device2.connect()

    disable_pulser()

#    send_run_cmd("STOP", 0, "/Data/BLOCKS/USBLF_PCGSC03/", "/home/ams/lontra/log.txt")

    N1081B_device1.start_acquisition(N1081B.Section.SEC_D, N1081B.FunctionType.FN_LUT)
    
    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tStarting BEAM trigger ...")

    disable_master_trigger()

    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tAll triggers disabled")

    reset_scalers()

#    send_run_cmd("START", 1, "/Data/BLOCKS/USBLF_PCGSC03/", "/home/ams/lontra/log.txt")
    
    enable_beam_trigger()

    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tBEAM triggers enabled")
