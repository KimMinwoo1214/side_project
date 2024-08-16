#include <Servo.h> // 서보모터 라이브러리를 포함

Servo ser;
int pos = 0; 

void setup() {
  ser.attach(10);
  pinMode(7, OUTPUT);       // Motor A 방향설정1
  pinMode(8, OUTPUT);       // Motor A 방향설정2
  pinMode(4, OUTPUT);       // Motor B 방향설정1
  pinMode(5, OUTPUT);       // Motor B 방향설정2
}



void loop() {
  for(pos = 0; pos < 180; pos++)
  {
    ser.write(pos);
    delay(15);
  }
  for(pos = 180; pos > 0; pos--)
  {
    ser.write(pos);
    delay(15);
  }

  /*모터A설정*/
  digitalWrite(7, HIGH);     // Motor A 방향설정1
  digitalWrite(8, LOW);      // Motor A 방향설정2
  analogWrite(9, 100);       // Motor A 속도조절 (0~255)

  /*모터B설정*/
  digitalWrite(4, LOW);      // Motor B 방향설정1
  digitalWrite(5, HIGH);     // Motor B 방향설정2
  analogWrite(3, 50);        // Motor B 속도조절 (0~255)
  delay(3000);                   // 3초 유지

  /*모터A설정*/
  digitalWrite(7, LOW);      // Motor A 방향설정1
  digitalWrite(8, HIGH);     // Motor A 방향설정2
  analogWrite(9, 200);      // Motor A 속도조절 (0~255)

  /*모터B설정*/
  digitalWrite(4, HIGH);    // Motor B 방향설정1
  digitalWrite(5, LOW);     // Motor B 방향설정2
  analogWrite(3, 150);      // Motor B 속도조절 (0~255)
  delay(3000);                    // 3초 유지
}