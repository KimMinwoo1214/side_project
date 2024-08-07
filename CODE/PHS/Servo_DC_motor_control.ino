#include <Servo.h>


const int SERVO = 3;
const int RightmotorR = 5;
const int RightmotorL = 6;
const int LeftmotorR = 10;
const int LeftmotorL =11;
Servo myServo;


void setup() {  
  //모터 제어
  pinMode(RightmotorR, OUTPUT);
  pinMode(RightmotorL, OUTPUT);
  pinMode(LeftmotorR, OUTPUT);
  pinMode(LeftmotorL, OUTPUT);

  //서보 제어
  myServo.attach(SERVO);
  myServo.write(90);

  
  //시리얼 통신
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();  // 문자열 양쪽의 공백 제거

    if (command == "front") {
      // 모터를 오른쪽으로 동작시키는 코드
      digitalWrite(RightmotorR, 255);
      digitalWrite(RightmotorL, 0);
      digitalWrite(LeftmotorR, 0);
      digitalWrite(LeftmotorL, 255);
      Serial.print("FRONT\n");
    }
    else if (command == "back") {
      // 모터를 오른쪽으로 동작시키는 코드
      digitalWrite(RightmotorR, 0);
      digitalWrite(RightmotorL, 255);
      digitalWrite(LeftmotorR, 255);
      digitalWrite(LeftmotorL, 0);
      Serial.print("back\n");
    } 
    else if (command == "right") {
      myServo.write(60);
    }
    else if (command == "left") {
      myServo.write(120);
    }
    else {
      // 모터를 정지시키는 코드
      digitalWrite(RightmotorR, LOW);
      digitalWrite(RightmotorL, LOW);
      digitalWrite(LeftmotorR, LOW);
      digitalWrite(LeftmotorL, LOW);
      // myServo.write(0);
    }
  }

}
