#include <RotaryEncoder.h>

#define S1 9      // PWM1 for Motor 1
#define D1 7      // Direction for Motor 1
#define S2 10     // PWM2 for Motor 2
#define D2 8      // Direction for Motor 2

#define ENCODER_A 2  // AMT103 Encoder Channel A
#define ENCODER_B 3  // AMT103 Encoder Channel B
#define INDEX_PIN 4  // AMT103 Encoder Index Pin (Interrupt)

const int PULSES_PER_REV = 1024; // AMT103 default PPR
volatile long rotationCount = 0;  // Full rotations detected by Index
unsigned long lastTime = 0;

// RotaryEncoder object
RotaryEncoder motorEncoder(ENCODER_A, ENCODER_B);

// ISR for Index Pin - Counts full revolutions
void countRevolutions() {
    rotationCount++;
}

// Function to set motor speed & direction based on PWM input
void setMotorControl(int pwm1, int pwm2) {
    int speed1 = constrain(map(pwm1, 5, 92, 255, 0), 0, 255);
    int speed2 = constrain(map(pwm2, 5, 92, 255, 0), 0, 255);

    if (pwm1 < 5) speed1 = 255;
    if (pwm2 < 5) speed2 = 255;
    if (pwm1 > 92) speed1 = 0;
    if (pwm2 > 92) speed2 = 0;

    if (pwm2 >= 5 && pwm2 <= 40) {
        digitalWrite(D1, LOW);
        digitalWrite(D2, LOW);
    } else if (pwm2 >= 57 && pwm2 <= 92) {
        digitalWrite(D1, HIGH);
        digitalWrite(D2, HIGH);
    } else if (pwm1 >= 5 && pwm1 <= 40) {
        digitalWrite(D1, LOW);
        digitalWrite(D2, HIGH);
    } else if (pwm1 >= 57 && pwm1 <= 92) {
        digitalWrite(D1, HIGH);
        digitalWrite(D2, LOW);
    }

    analogWrite(S1, speed1);
    analogWrite(S2, speed2);
}

void setup() {
    pinMode(S1, OUTPUT);
    pinMode(D1, OUTPUT);
    pinMode(S2, OUTPUT);
    pinMode(D2, OUTPUT);
    
    pinMode(INDEX_PIN, INPUT_PULLUP);
    
    attachInterrupt(digitalPinToInterrupt(INDEX_PIN), countRevolutions, RISING);

    Serial.begin(9600);
}

void loop() {
    // Example test values (adjust as needed)
    int pwm1 = 30;
    int pwm2 = 70;
    setMotorControl(pwm1, pwm2);

    motorEncoder.tick(); // Update encoder readings

    unsigned long currentTime = millis();
    if (currentTime - lastTime >= 1000) {
        long encoderPulses = motorEncoder.getPosition();
        float calculatedRotations = (float)encoderPulses / PULSES_PER_REV;

        Serial.print("Total Rotations (from pulses): ");
        Serial.println(calculatedRotations);
        Serial.print("Full Rotations (from index pin): ");
        Serial.println(rotationCount);

        lastTime = currentTime;
    }
}
