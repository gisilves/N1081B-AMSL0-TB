import sys
from datetime import datetime
from N1081B_sdk import N1081B

def disable_master_trigger():
    N1081B_device1.configure_digital_generator(N1081B.Section.SEC_C,False,False,False,False)

def enable_calibration():
    N1081B_device1.configure_digital_generator(N1081B.Section.SEC_C,False,True,False,False)

def reset_scalers():
    N1081B_device2.reset_channel(N1081B.Section.SEC_D,0,N1081B.FunctionType.FN_SCALER)
    N1081B_device2.reset_channel(N1081B.Section.SEC_D,1,N1081B.FunctionType.FN_SCALER)
    N1081B_device2.reset_channel(N1081B.Section.SEC_D,2,N1081B.FunctionType.FN_SCALER)
    N1081B_device2.reset_channel(N1081B.Section.SEC_D,3,N1081B.FunctionType.FN_SCALER)

    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tScalers reset before calibration trigger")

if __name__ == "__main__":
    
    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tStarting calibration trigger ...")

    N1081B_device1 = N1081B("pool05940004.cern.ch")
    N1081B_device1.connect()

    N1081B_device2 = N1081B("pool05940001.cern.ch")
    N1081B_device2.connect()

    disable_master_trigger()
    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tAll triggers disabled")

    reset_scalers()

    enable_calibration()
    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S") + "\tCalibration enabled")
