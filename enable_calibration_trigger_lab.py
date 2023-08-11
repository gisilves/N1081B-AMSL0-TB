import sys
from datetime import datetime
from N1081B_sdk import N1081B

def enable_calibration():
    N1081B_device1.configure_digital_generator(N1081B.Section.SEC_C,True,True,False,False)

def enable_master_trigger():
    N1081B_device2.set_output_channel_configuration(N1081B.Section.SEC_C,0,True,True,1000,False)
    N1081B_device2.set_output_channel_configuration(N1081B.Section.SEC_C,1,True,False,0,False)

def reset_scalers():
    N1081B_device2.reset_channel(N1081B.Section.SEC_D,0,N1081B.FunctionType.FN_SCALER)
    N1081B_device2.reset_channel(N1081B.Section.SEC_D,1,N1081B.FunctionType.FN_SCALER)

    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tScalers reset before calibration trigger")

def disable_fake_spill():
    #Retrieve SEC_D configuration
    current_config = N1081B_device1.get_function_configuration(N1081B.Section.SEC_D)
    # Retrieve the 'enable' value for fake busy from current_config
    target_lemo = 2
    lemo_enables = current_config['data']['lemo_enables']
    fake_busy = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)
    N1081B_device1.configure_digital_generator(N1081B.Section.SEC_D,False,False,fake_busy,False)

if __name__ == "__main__":
    
    N1081B_device1 = N1081B("pool05940004.cern.ch")
    N1081B_device1.connect()

    N1081B_device2 = N1081B("pool05940001.cern.ch")
    N1081B_device2.connect()

    reset_scalers()

    enable_calibration()
    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tCalibration enabled")

    disable_fake_spill()
    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tFake spill disabled (LAB TESTS ONLY)")

    enable_master_trigger()
    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tTriggers enabled")
