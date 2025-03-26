from machine import Pin, PWM
import time


Flywheel Motor	                        GP0
Defense Arm Motor (Closing)	            GP1
Defense Arm Motor (Raising - Left)	    GP2
Defense Arm Motor (Raising - Right)	    GP3
Retractable Hood Motor              	GP4
Limit Switch (Closed - Hands)   	    GP5
Limit Switch (Open - Hands)            	GP6
Limit Switch (Raised - Arms)	        GP7
Limit Switch (Lowered - Arms)       	GP8
IR Detector (Ball Tracking)	            GP9


from machine import Pin, PWM, Timer

# === Motor PWM Configuration ===
PWM_FREQ = 16000  # 16kHz frequency for motors

flywheel = PWM(Pin(0))  # Flywheel Motor
defense_motor = PWM(Pin(1))  # Defense Arm Motor
hood_motor = PWM(Pin(2))  # Retractable Hood Motor

flywheel.freq(PWM_FREQ)
defense_motor.freq(PWM_FREQ)
hood_motor.freq(PWM_FREQ)

# === Servo Configuration ===
servo = PWM(Pin(5))  # Flap Servo
servo.freq(50)  # Standard 50Hz for servos

# === Limit Switches ===
limit_closed = Pin(6, Pin.IN, Pin.PULL_UP)  # Fully closed position
limit_open = Pin(7, Pin.IN, Pin.PULL_UP)  # Fully open position

# === IR Detector ===
ir_sensor = Pin(8, Pin.IN, Pin.PULL_UP)  # Ball detection

# === Motor Control Functions ===
def set_motor(motor, duty):
    """Set PWM duty cycle (0 to 65535)"""
    motor.duty_u16(duty)

def stop_motor(motor):
    """Stop the motor by setting duty cycle to 0"""
    motor.duty_u16(0)

def set_servo(angle):
    """Move servo to a specific angle (0° to 180°)"""
    duty = int(1638 + (angle / 180) * (8192 - 1638))  # Convert angle to duty
    servo.duty_u16(duty)

# === Timer-Based Limit Switch Check ===
def check_defense_motor(timer):
    """Stops the defense motor when limits are reached"""
    if limit_closed.value() == 0:  # If fully closed
        stop_motor(defense_motor)
    elif limit_open.value() == 0:  # If fully open
        stop_motor(defense_motor)

# === Timer-Based IR Detection for Flap ===
def check_flap(timer):
    """Stops flap movement when the ball is detected"""
    if ir_sensor.value() == 0:  # Ball detected
        stop_motor(servo)

# === Timers for Continuous Checking (Non-blocking) ===
timer1 = Timer()
timer1.init(period=100, mode=Timer.PERIODIC, callback=check_defense_motor)

timer2 = Timer()
timer2.init(period=100, mode=Timer.PERIODIC, callback=check_flap)

# === Example Motor Control ===
set_motor(flywheel, 40000)  # Run flywheel at ~60% speed
set_motor(defense_motor, 30000)  # Start closing defense arms
set_motor(hood_motor, 50000)  # Extend hood at ~80% speed
set_servo(90)  # Move flap to 90 degrees

# Main loop does not use delay() to avoid blocking other tasks
while True:
    pass  # Timers handle limit switch and IR sensor events
