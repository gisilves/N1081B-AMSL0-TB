import numpy as np
import argparse
from N1081B_sdk import N1081B

# --- User-configurable constants ---------------------------------------------
INTERNAL_CLOCK_HZ = 10_000_000      # 10 MHz internal clock
PULSE_WIDTH_NS    = 200             # Pulse width (monostable) in ns
FRAME_INTERVAL_MS = 8               # Period between successive double pulses
SECTION_INDEX     = 0               # Index of the section to use
# -----------------------------------------------------------------------------


def generate_double_pulse(device, pulse_gap_us):
    """
    Generate two digital pulses with a fixed width and a programmable gap between them.
    
    """

    tick_duration_s = 1 / INTERNAL_CLOCK_HZ             # Clock tick duration in seconds (e.g., 100 ns)
    pulse_width_ticks = max(1, round(PULSE_WIDTH_NS * 1e-9 / tick_duration_s))
    gap_ticks = round(pulse_gap_us * 1e-6 / tick_duration_s)
    frame_length_ticks = round(FRAME_INTERVAL_MS * 1e-3 / tick_duration_s)

    if gap_ticks < 1 or (gap_ticks + 2 * pulse_width_ticks > frame_length_ticks):
        raise ValueError(f"Invalid pulse_gap_us={pulse_gap_us}. "
                         f"Must be ≥ {tick_duration_s * 1e6:.1f} µs and "
                         f"gap + 2 x width must fit within {FRAME_INTERVAL_MS} ms frame.")

    pattern = np.zeros(frame_length_ticks, dtype=np.uint32)
    pattern[0:pulse_width_ticks] = 1                                   # First pulse at t = 0
    pattern[pulse_width_ticks + gap_ticks : pulse_width_ticks + gap_ticks + pulse_width_ticks] = 1  # Second pulse

    section = device.section(SECTION_INDEX)
    section.set_function("PATTERN_GENERATOR")
    section.pg.clock_source = "INTERNAL"
    section.pg.clock_rate   = INTERNAL_CLOCK_HZ
    section.pg.load_pattern(pattern)
    section.pg.start(cyclic=True)

    print(f"Double pulse pattern loaded: {pulse_gap_us} µs gap, "
          f"{PULSE_WIDTH_NS} ns width, frame = {FRAME_INTERVAL_MS} ms")


# -----------------------------------------------------------------------------


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a programmable double pulse using CAEN N1081B")
    parser.add_argument("--delta_us", type=float, default=200,
                        help="Gap between two pulses in microseconds (e.g. 200)")
    parser.add_argument("--ip", type=str, default="pool05940004.cern.ch",
                        help="IP address or hostname of the N1081B device")
    parser.add_argument("--password", type=str, default="12345",
                        help="Password for the device login")
    args = parser.parse_args()

    device = N1081B(args.ip)

    try:
        device.connect()
        device.login(args.password)
        generate_double_pulse(device, pulse_gap_us=args.delta_us)
    finally:
        device.disconnect()
        print("Disconnected from device.")
