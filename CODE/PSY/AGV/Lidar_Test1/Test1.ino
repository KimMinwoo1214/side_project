#include <SoftwareSerial.h>

// 소프트웨어 시리얼을 사용하여 RPLidar와 통신
SoftwareSerial lidarSerial(11, 10); // RX, TX 핀 정의

const int motorPin = 9; // 모터 제어를 위한 핀 정의

void setup() {
  Serial.begin(115200); // 시리얼 모니터와 통신 시작
  lidarSerial.begin(115200); // LiDAR와 통신 시작

  pinMode(motorPin, OUTPUT); // 모터 핀을 출력으로 설정
  analogWrite(motorPin, 255); // 모터를 최대 속도로 회전
  Serial.println("LiDAR and Motor initialized...");
}

void loop() {
  if (lidarSerial.available()) {
    // LiDAR에서 데이터 읽기
    byte data = lidarSerial.read();
    Serial.print("Received data: ");
    Serial.println(data, HEX); // 데이터 출력 (헥사 형식)
  }
  delay(10); // 딜레이
}