#include <Servo.h>  // 서보 모터 제어 라이브러리

int ENA = 10;  // 모터 1 속도 제어 핀 (PWM 핀)
int IN1 = 3;   // 모터 1 방향 제어 핀 (디지털 핀)
int IN2 = 5;   // 모터 1 방향 제어 핀 (디지털 핀)
int ENB = 11;  // 모터 2 속도 제어 핀 (PWM 핀)
int IN3 = 6;   // 모터 2 방향 제어 핀 (디지털 핀)
int IN4 = 7;   // 모터 2 방향 제어 핀 (디지털 핀)

Servo myServo;  // 서보 모터 객체 생성
int servoPin = 9;  // 서보 모터 제어 핀 (PWM 핀)

int speedValue = 0;  // 초기 속도 값
int servoAngle = 90; // 서보 모터 초기 각도

void setup() {
  Serial.begin(9600);  // 시리얼 통신 시작
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  myServo.attach(servoPin);  // 서보 모터 핀 설정
  myServo.write(servoAngle); // 초기 각도로 서보 모터 설정 (90도)
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');  // 파이썬에서 받은 명령어와 속도를 문자열로 읽음
    char command = input.charAt(0);  // 명령어 추출
    int value = input.substring(1).toInt();  // 속도 또는 각도 값 추출

    if (command == 'G') {
      // 모터 전진
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      analogWrite(ENA, value);  // 설정된 속도로 모터 1 구동
      analogWrite(ENB, value);  // 설정된 속도로 모터 2 구동
    }
    else if (command == 'B') {
      // 모터 후진
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      analogWrite(ENA, value);  // 설정된 속도로 모터 1 구동
      analogWrite(ENB, value);  // 설정된 속도로 모터 2 구동
    }
    else if (command == 'S') {
      // 모터 정지
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
    }
    else if (command == 'A') {
      // 서보 모터 각도 조절
      if (value >= 0 && value <= 180) {
        myServo.write(value);  // 서보 모터를 입력된 각도로 이동
      }
    }
  }
}