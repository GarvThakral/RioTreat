#include <Servo.h>
#include <string.h>
Servo myservo;
int servoPin = 11;

void setup() {
  myservo.attach(servoPin);
  Serial.begin(9600);
}

void loop() {
  while(!Serial.available());
  String input = Serial.readStringUntil('\n');
  int angle = input.toInt();               
  myservo.write(angle);
  delay(1000);
}
