import time
import argparse
from N1081B_sdk import N1081B

def poisson_trigger(device, avg_freq, duration):
    if duration == -1:
        print("Generating Poisson distributed pulses with an average frequency of {} Hz".format(avg_freq))
        device.configure_pulse_generator(N1081B.Section.SEC_D,
                                            N1081B.StatisticMode.STAT_POISSON,
                                            250, avg_freq, True, True, True, True)
    else:
        print("Generating Poisson distributed pulses with an average frequency of {} Hz for {} seconds".format(avg_freq, duration))
        device.configure_pulse_generator(N1081B.Section.SEC_D,
                                            N1081B.StatisticMode.STAT_POISSON,
                                            250, avg_freq, True, True, True, True)
        seconds = 1
        while seconds <= duration:
            print("Seconds: {}\r".format(seconds), end="")
            seconds += 1
            time.sleep(1)
        
        print("Done")
        device.configure_pulse_generator(N1081B.Section.SEC_D,
                                            N1081B.StatisticMode.STAT_POISSON,
                                            250, avg_freq, False, False, False, False)

# -----------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a programmable double pulse using CAEN N1081B")
    parser.add_argument("--avg_freq", type=float, default=200,
                        help="Average frequency of Poission distributed pulses in Hz")
    parser.add_argument("--duration", type=float, default=-1,
                        help="Time the pulses are generated for in seconds (default: -1 for infinite)")
    parser.add_argument("--ip", type=str, default="pool05940004.cern.ch",
                        help="IP address or hostname of the N1081B device")
    parser.add_argument("--password", type=str, default="12345",
                        help="Password for the device login")
    args = parser.parse_args()

    device = N1081B(args.ip)

    try:
        device.connect()
        device.login(args.password)
        poisson_trigger(device, args.avg_freq, args.duration)
    finally:
        device.disconnect()
        print("Disconnected from device.")
