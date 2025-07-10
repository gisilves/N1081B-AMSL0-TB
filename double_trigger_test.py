import numpy as np
import argparse
from N1081B_sdk import N1081B
import time

def generate_double_pulse(device, pulse_gap_us):

    """
    Generate two digital pulses with a fixed width and a programmable gap between them.

    The second pulse is triggered by the first pulse and is delayed by the requested gap
    with a OR gate.
    """

    # Set section A function as pulse generator
    device.set_section_function(N1081B.Section.SEC_A,
                                    N1081B.FunctionType.FN_PULSE_GENERATOR)

    device.configure_pulse_generator(N1081B.Section.SEC_A,
                                     N1081B.StatisticMode.STAT_DETERMINISTIC,
                                     1000, 8000000, True, False, True, False)
    
    # Set outputs to TTL
    device.set_output_configuration(N1081B.Section.SEC_A,
                                     N1081B.SignalStandard.STANDARD_TTL)
    device.set_output_configuration(N1081B.Section.SEC_B,
                                     N1081B.SignalStandard.STANDARD_TTL)
    

    # Set section B function as OR + Veto
    device.set_section_function(N1081B.Section.SEC_B,
                                    N1081B.FunctionType.FN_OR_VETO)
    
    device.configure_or_veto(N1081B.Section.SEC_B,
                             True, True, False, False, False, False, 0)
    
    device.set_input_configuration(N1081B.Section.SEC_B,
                                    N1081B.SignalStandard.STANDARD_TTL,
                                    N1081B.SignalStandard.STANDARD_TTL,
                                    0,
                                    N1081B.SignalImpedance.IMPEDANCE_50)  

    # Configure the gap between the two pulses
    device.set_input_channel_configuration(N1081B.Section.SEC_B,
                                            1,
                                            True,
                                            True,
                                            1000,
                                            int(pulse_gap_us)*500,
                                            False)
    
    # Set section C function as OR + Veto
    device.set_section_function(N1081B.Section.SEC_C,
                                    N1081B.FunctionType.FN_OR_VETO)
    
    device.configure_or_veto(N1081B.Section.SEC_C,
                             True, True, False, False, False, False, 0)
    
    device.set_input_configuration(N1081B.Section.SEC_C,
                                    N1081B.SignalStandard.STANDARD_TTL,
                                    N1081B.SignalStandard.STANDARD_TTL,
                                    0,
                                    N1081B.SignalImpedance.IMPEDANCE_50)


    # Configure the gap between the two pulses
    device.set_input_channel_configuration(N1081B.Section.SEC_C,
                                            1,
                                            True,
                                            True,
                                            1000,
                                            int(pulse_gap_us)*500,
                                            False)  
    

    print("Generated double pulse with a gap of {} us".format(pulse_gap_us))


# -----------------------------------------------------------------------------

def main(args, device):
    if not args.sweep:
        generate_double_pulse(device, args.delta_us)
    else:
        for delta_us in np.arange(args.min_delta_us, args.max_delta_us, args.step):
            generate_double_pulse(device, delta_us)
            time.sleep(args.duration)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a programmable double pulse using CAEN N1081B")
    parser.add_argument("--delta_us", type=float, default=200,
                        help="Gap between two pulses in microseconds (default: 200)")
    parser.add_argument("--ip", type=str, default="pool05940011.cern.ch",
                        help="IP address or hostname of the N1081B device")
    parser.add_argument("--password", type=str, default="password",
                        help="Password for the device login")
    parser.add_argument("--min_delta_us", type=float, default=200,
                        help="Minimum gap between two pulses in microseconds (default: 1)")
    parser.add_argument("--max_delta_us", type=float, default=1200,
                        help="Maximum gap between two pulses in microseconds (default: 200)")
    parser.add_argument("--sweep", action='store_true',
                        help="Enable sweeping the gap between two pulses")
    parser.add_argument("--step", type=float, default=100,
                        help="Step size for the gap sweep in microseconds (default: 1)")
    parser.add_argument("--duration", type=float, default=5,
                        help="Duration of each sweep step in seconds (default: 5)")
    args = parser.parse_args()

    device = N1081B(args.ip)

    try:
        device.connect()
        device.login(args.password)
        main(args, device)
    finally:
        device.disconnect()
        print("Disconnected from device.")
