#include <SoftwareSerial.h>

SoftwareSerial urt1Serial(10, 11); // RX, TX

void setup() {
  urt1Serial.begin(1000000); // URT-1과의 통신 속도 설정
}

void loop() {
  for (int angle = 0; angle <= 180; angle += 10) {
    setServoAngle(2, angle); // ID 2의 서보 모터 각도 설정
    delay(500); // 각도 변경 간의 대기 시간
  }
}

void setServoAngle(int id, int angle) {
  byte command[6];
  command[0] = 0xFF; // 시작 바이트
  command[1] = id;   // 서보 모터 ID
  command[2] = 0x06; // 명령 길이
  command[3] = 0x03; // 서보 모터 각도 설정 명령
  command[4] = angle; // 설정할 각도
  command[5] = 0;     // 체크섬 (적절한 값으로 설정해야 함)

  // 체크섬 계산
  for (int i = 1; i < 5; i++) {
    command[5] += command[i];
  }
  command[5] = ~command[5];

  urt1Serial.write(command, sizeof(command)); // 명령 전송
}
