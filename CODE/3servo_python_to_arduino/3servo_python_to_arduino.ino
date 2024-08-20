#include <Servo.h>

// 서보 객체 생성
Servo servo1;
Servo servo2;
Servo servo3;

// 서보 모터를 연결할 핀 번호 설정
int servo1Pin = 2;
int servo2Pin = 5;
int servo3Pin = 6;

void setup() {
  // 서보 핀과 객체 연결
  servo1.attach(servo1Pin);
  servo2.attach(servo2Pin);
  servo3.attach(servo3Pin);

  // 시리얼 통신 시작
  Serial.begin(9600);
  Serial.println("파이썬에서 서보모터 각도를 입력하세요 (예: 90, 45, 120)");
}

void loop() {
  // 시리얼 데이터가 있는지 확인
  if (Serial.available() > 0) {
    // 시리얼로 들어온 데이터 읽기
    String input = Serial.readStringUntil('\n');

    // 쉼표를 기준으로 데이터를 분리
    int firstComma = input.indexOf(',');
    int secondComma = input.indexOf(',', firstComma + 1);

    // 입력된 각도 추출
    if (firstComma != -1 && secondComma != -1) {
      int angle1 = input.substring(0, firstComma).toInt();
      int angle2 = input.substring(firstComma + 1, secondComma).toInt();
      int angle3 = input.substring(secondComma + 1).toInt();

      // 각도를 0~180도로 제한
      angle1 = constrain(angle1, 0, 180);
      angle2 = constrain(angle2, 0, 180);
      angle3 = constrain(angle3, 0, 180);

      // 서보 위치 설정
      servo1.write(angle1);
      servo2.write(angle2);
      servo3.write(angle3);

      // 결과 출력
      Serial.print("Servo 1: ");
      Serial.print(angle1);
      Serial.print(" degrees, Servo 2: ");
      Serial.print(angle2);
      Serial.print(" degrees, Servo 3: ");
      Serial.print(angle3);
      Serial.println(" degrees");
    } else {
      // 잘못된 입력 처리
      Serial.println("잘못된 입력입니다. 형식: 90, 45, 120");
    }
  }
}
