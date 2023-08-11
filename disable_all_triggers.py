import sys
from datetime import datetime
from N1081B_sdk import N1081B

def disable_calibration():
    N1081B_device1.configure_digital_generator(N1081B.Section.SEC_C,False,False,False,False)

def disable_master_trigger():
    N1081B_device2.set_output_channel_configuration(N1081B.Section.SEC_C,0,False,True,1000,False)
    N1081B_device2.set_output_channel_configuration(N1081B.Section.SEC_C,1,False,False,0,False)

def read_scalers():
    current_config = N1081B_device2.get_function_results(N1081B.Section.SEC_D)
    target_lemo = 0
    lemo_counters = current_config['data']['counters']
    scaler_1 = next(item['value'] for item in lemo_counters if item['lemo'] == target_lemo)
    
    target_lemo = 1
    lemo_counters = current_config['data']['counters']
    scaler_2 = next(item['value'] for item in lemo_counters if item['lemo'] == target_lemo)

    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tTotal scintillator coincidences: " + str(scaler_1) + "\tTotal triggers: " + str(scaler_2))

if __name__ == "__main__":
    
    N1081B_device1 = N1081B("pool05940004.cern.ch")
    N1081B_device1.connect()

    N1081B_device2 = N1081B("pool05940001.cern.ch")
    N1081B_device2.connect()

    disable_calibration()
    disable_master_trigger()
    
    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tTriggers disabled")

    read_scalers()