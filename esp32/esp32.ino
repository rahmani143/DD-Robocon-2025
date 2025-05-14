#include <IBusBM.h>
IBusBM ibus;

void setup() {
  Serial.begin(115200);       
  Serial2.begin(115200, SERIAL_8N1, 16, 17); 
  ibus.begin(Serial2);             
  Serial1.begin(9600, SERIAL_8N1, 4, 5);
}

void loop() {
  ibus.loop();

  for (int ch = 0; ch < 4; ch++) {
    if (ch != 2){
      int val = ibus.readChannel(ch);
      Serial.print("CH");
      Serial1.print("CH");
      Serial.print(ch + 1);
      Serial1.print(ch + 1);
      Serial.print(": ");
      Serial1.print(": ");
      Serial.print(float(val - 1000) / 1000);
      Serial1.print(float(val - 1000) / 1000);
      Serial.print("\t");
      Serial1.print("\t");
    }
  }
  Serial.println();
  Serial1.println();
  delay(100);  
}
