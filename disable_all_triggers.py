import sys
from datetime import datetime
from N1081B_sdk import N1081B
#from client_charge_tagger_L0BT_20231022 import *

def disable_master_trigger():
    N1081B_device1.configure_digital_generator(N1081B.Section.SEC_C,False,False,False,False)

def disable_pulser():
    N1081B_device1.configure_pulse_generator(N1081B.Section.SEC_B,
                                             N1081B.StatisticMode.STAT_DETERMINISTIC,
                                             250, 100000000, False, False, False, False)

def read_scalers():
    current_config = N1081B_device2.get_function_results(N1081B.Section.SEC_D)

    target_lemo = 0
    lemo_counters = current_config['data']['counters']
    scaler_0 = next(item['value'] for item in lemo_counters if item['lemo'] == target_lemo)
    
    target_lemo = 1
    lemo_counters = current_config['data']['counters']
    scaler_1 = next(item['value'] for item in lemo_counters if item['lemo'] == target_lemo)

    target_lemo = 2
    lemo_counters = current_config['data']['counters']
    scaler_2 = next(item['value'] for item in lemo_counters if item['lemo'] == target_lemo)

    target_lemo = 3
    lemo_counters = current_config['data']['counters']
    scaler_3 = next(item['value'] for item in lemo_counters if item['lemo'] == target_lemo)
    
    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tTotal beam triggers: " + str(scaler_1))
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tTotal cal triggers: " + str(scaler_0))
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tTotal triggers: " + str(scaler_2))
#    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tTotal busy: " + str(scaler_3))
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tTotal scintillator ANDs: " + str(scaler_3))

if __name__ == "__main__":
    
    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tStopping all triggers ...")

    N1081B_device1 = N1081B("caenplu-perugia1.cern.ch")
    N1081B_device1.connect()

    N1081B_device2 = N1081B("caenplu-perugia2.cern.ch")
    N1081B_device2.connect()

    disable_master_trigger()
    disable_pulser()
    
#    send_run_cmd("STOP", 0, "/Data/BLOCKS/USBLF_PCGSC03/", "/home/ams/lontra/log.txt")

    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tAll Triggers disabled")

    read_scalers()
