from machine import Pin
import time

# Encoder pin definitions
ENCODER_A = Pin(14, Pin.IN, Pin.PULL_UP)
ENCODER_B = Pin(15, Pin.IN, Pin.PULL_UP)

# Encoder settings
PULSES_PER_REV = 1000  # Adjust this based on your encoder specs

# Variables
pulse_count = 0
last_state = ENCODER_A.value()
start_time = time.ticks_ms()  # Start time

# Run for a fixed duration
MEASURE_TIME = 5  # Measure for 5 seconds

while time.ticks_diff(time.ticks_ms(), start_time) < MEASURE_TIME * 1000:
    current_state = ENCODER_A.value()
    
    if last_state != current_state:  # Detect pulse change
        if ENCODER_B.value() != current_state:
            pulse_count += 1
        else:
            pulse_count -= 1
    
    last_state = current_state

# Calculate total rotations
total_rotations = pulse_count / PULSES_PER_REV

print("Total Rotations in", MEASURE_TIME, "seconds:", total_rotations)
