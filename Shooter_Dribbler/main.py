from machine import Pin, PWM
import time


# there is 1 motor for the flywheel
# there are 3 motors for the defensive mechanism 
#           - 1 for the closing of hands
#           - 2 for the raising of the arms
# there is 1 motor for the retractable hood
# total = 5 motors


# Assigning PWM pins to motors
flywheel_motor = PWM(Pin(2))   # GP2 - Flywheel Motor
hand_motor = PWM(Pin(3))       # GP3 - Closing Hands
arm_left_motor = PWM(Pin(4))   # GP4 - Left Arm Raise
arm_right_motor = PWM(Pin(5))  # GP5 - Right Arm Raise
hood_motor = PWM(Pin(6))       # GP6 - Retractable Hood


# Set PWM frequency for all motors
MOTOR_FREQ = 1000  # 1kHz PWM frequency
for motor in [flywheel_motor, hand_motor, arm_left_motor, arm_right_motor, hood_motor]:
    motor.freq(MOTOR_FREQ)

# Function to set motor speed (0-65535)
def set_motor_speed(motor, speed):
    """ Set PWM duty cycle (0 = OFF, 65535 = Full Speed) """
    motor.duty_u16(speed)

# Stop all motors initially
def stop_all_motors():
    for motor in [flywheel_motor, hand_motor, arm_left_motor, arm_right_motor, hood_motor]:
        set_motor_speed(motor, 0)

# Example usage
stop_all_motors()  # Ensure all motors are off initially

try:
    while True:
        # Test sequence - Modify based on your needs
        
        # Start Flywheel Motor at 75% Speed
        set_motor_speed(flywheel_motor, 49152)  
        time.sleep(2)

        # Close Hands (50% Speed)
        set_motor_speed(hand_motor, 32768)
        time.sleep(1)

        # Raise Arms (Left & Right at 60% Speed)
        set_motor_speed(arm_left_motor, 39321)
        set_motor_speed(arm_right_motor, 39321)
        time.sleep(2)

        # Extend Retractable Hood (Full Speed)
        set_motor_speed(hood_motor, 65535)
        time.sleep(3)

        # Stop all motors
        stop_all_motors()
        time.sleep(2)

except KeyboardInterrupt:
    stop_all_motors()  # Ensure motors stop when exiting