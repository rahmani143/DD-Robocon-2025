from machine import Pin, PWM, Timer
import time

# === Pin Configuration ===
# Flywheel Motor → GPIO0
# Defense Arm Motor (Closing) → GPIO1
# Defense Arm Motor (Raising - Left) → GPIO2
# Defense Arm Motor (Raising - Right) → GPIO3
# Retractable Hood Motor → GPIO4
# Servo (Flap) → GPIO5

# Limit Switches
# Fully Closed (Hands) → GPIO6
# Fully Open (Hands) → GPIO7
# IR Detector (Ball Tracking) → GPIO8

# Encoder
# A (CHA) → GPIO9
# B (CHB) → GPIO10
# Z (Index) → GPIO11 (optional)

# === Constants ===
PWM_FREQ = 16000          # 16kHz PWM frequency
ENCODER_PULSES_PER_REV = 500  # Adjust based on your encoder's spec
TARGET_RPM = 1069          # Scaled target RPM

# === Motor & Servo Configuration ===
flywheel = PWM(Pin(0))
defense_motor = PWM(Pin(1))
hood_motor = PWM(Pin(2))

flywheel.freq(PWM_FREQ)
defense_motor.freq(PWM_FREQ)
hood_motor.freq(PWM_FREQ)

servo = PWM(Pin(5))
servo.freq(50)  # 50Hz for servo

# === Limit Switches ===
limit_closed = Pin(6, Pin.IN, Pin.PULL_UP)
limit_open = Pin(7, Pin.IN, Pin.PULL_UP)

# === IR Detector ===
ir_sensor = Pin(8, Pin.IN, Pin.PULL_UP)

# === Encoder Pins ===
encoder_a = Pin(9, Pin.IN, Pin.PULL_UP)
encoder_b = Pin(10, Pin.IN, Pin.PULL_UP)
encoder_z = Pin(11, Pin.IN, Pin.PULL_UP)  # Optional Index pulse

# === Variables for Encoder Tracking ===
encoder_count = 0
last_time = time.ticks_ms()

# === Motor Control Functions ===
def set_motor(motor, duty):
    """Set PWM duty cycle (0 to 65535)"""
    motor.duty_u16(duty)

def stop_motor(motor):
    """Stop the motor by setting duty cycle to 0"""
    motor.duty_u16(0)

def set_servo(angle):
    """Move servo to a specific angle (0° to 180°)"""
    duty = int(1638 + (angle / 180) * (8192 - 1638))
    servo.duty_u16(duty)

# === Encoder ISR ===
def encoder_isr(pin):
    """Handles encoder pulse counting with direction detection"""
    global encoder_count
    if encoder_a.value() == encoder_b.value():
        encoder_count += 1   # Clockwise
    else:
        encoder_count -= 1   # Counter-clockwise

# === RPM Calculation and Feedback Adjustment ===
def update_rpm(timer):
    """Calculate RPM and adjust motor speed accordingly"""
    global encoder_count, last_time

    current_time = time.ticks_ms()
    time_diff = time.ticks_diff(current_time, last_time) / 1000  # in seconds

    # Calculate RPM
    if time_diff > 0:
        rpm = (encoder_count / ENCODER_PULSES_PER_REV) * (60 / time_diff)
    else:
        rpm = 0

    encoder_count = 0
    last_time = current_time

    # Adjust motor speed if RPM drifts from the target
    if rpm < TARGET_RPM:
        new_duty = min(flywheel.duty_u16() + 2000, 65535)
        flywheel.duty_u16(new_duty)
    elif rpm > TARGET_RPM:
        new_duty = max(flywheel.duty_u16() - 2000, 0)
        flywheel.duty_u16(new_duty)

    print(f"RPM: {rpm}, Adjusted Duty: {flywheel.duty_u16()}")

# === Timer-Based Limit Switch Check ===
def check_defense_motor(timer):
    """Stops defense motor when limit switches are triggered"""
    if limit_closed.value() == 0:  # Closed position
        stop_motor(defense_motor)
    elif limit_open.value() == 0:  # Open position
        stop_motor(defense_motor)

# === Timer-Based IR Detection for Flap Control ===
def check_flap(timer):
    """Stops flap when ball is detected"""
    if ir_sensor.value() == 0:
        stop_motor(servo)

# === Attach Interrupts for Encoder Channels ===
encoder_a.irq(trigger=Pin.IRQ_RISING, handler=encoder_isr)
encoder_b.irq(trigger=Pin.IRQ_RISING, handler=encoder_isr)

# === Timers for Non-blocking Execution ===
timer1 = Timer()
timer1.init(period=100, mode=Timer.PERIODIC, callback=check_defense_motor)

timer2 = Timer()
timer2.init(period=100, mode=Timer.PERIODIC, callback=check_flap)

timer3 = Timer()
timer3.init(period=500, mode=Timer.PERIODIC, callback=update_rpm)

# === Example Motor Control ===
set_motor(flywheel, 30000)  # Start flywheel at 50% speed
set_motor(defense_motor, 20000)  # Defense arms at moderate speed
set_motor(hood_motor, 40000)  # Extend hood at 60% speed
set_servo(90)  # Move servo to 90 degrees

# === Main Loop (Idle, timers handle events) ===
while True:
    pass
