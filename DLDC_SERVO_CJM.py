#include <Servo.h>

// 서보 모터 핀 정의
Servo myServo;
int servoPin = 9;

// DC 모터 핀 정의 
int in1 = 8;
int in2 = 7;


void setup() {
  // 서보 모터 초기화
  myServo.attach(servoPin);
  
  // DC 모터 핀을 출력으로 설정
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
 

  // 초기 모터 상태 설정

  myServo.write(90);   // 서보 모터 중간 위치
}

void loop() {
  // 서보 모터와 DC 모터를 동시에 제어
  for (int pos = 0; pos <= 180; pos += 1) {
    myServo.write(pos);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);

    delay(15);
  }

  for (int pos = 180; pos >= 0; pos -= 1) {
    myServo.write(pos);
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);

    delay(15);
  }

  // DC 모터 정지


}