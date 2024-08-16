#include <Servo.h>

Servo myServo;
int servoPin = 3;
int angle = 0; // 입력된 각도를 저장할 변수

void setup() {
  myServo.attach(servoPin);
  Serial.begin(9600); // 시리얼 통신 시작
}

void loop() {
  if (Serial.available() > 0) { // 시리얼 데이터를 수신했을 때
    angle = Serial.parseInt(); // 시리얼 데이터(정수)를 읽음

    if (angle >= 0 && angle <= 180) { // 유효한 각도 범위 확인
      myServo.write(angle); // 서보 모터를 입력된 각도로 회전
      Serial.print("서보 모터 각도: ");
      Serial.println(angle); // 현재 각도를 시리얼로 출력
    } else {
      Serial.println("잘못된 각도입니다. 0에서 180 사이의 값을 보내세요.");
    }
  }
}