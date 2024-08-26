#define SERVO_PIN 3          // 서보 모터가 연결된 핀
#define SERVO_PERIOD 20000   // 20ms (서보 모터의 주기)

int lastAngle = -1;  // 마지막 각도를 저장하는 변수 (초기값은 -1)

void setup() {
  pinMode(SERVO_PIN, OUTPUT);  // 3번 핀을 출력으로 설정
  Serial.begin(115200);  // 기본 시리얼 통신 (PC 또는 Jetson Nano와 연결용)
  
  Serial.println("Enter an angle between 0 and 180:");
}

void loop() {
  if (Serial.available() > 0) {  // 기본 시리얼로 데이터가 들어오면
    String input = Serial.readStringUntil('\n');  // 줄바꿈까지 데이터를 읽음
    input.trim();  // 공백 제거

    if (input.length() > 0) {
      int angle = input.toInt();  // 입력된 값을 각도로 변환

      // 입력된 각도가 유효한지 확인
      if (angle >= 0 && angle <= 180 && angle != lastAngle) {
        int pulseWidth = angleToPulseWidth(angle);  // 각도를 펄스 폭으로 변환
        moveServo(pulseWidth);  // 해당 펄스 폭으로 서보 모터 움직임
        Serial.print("Moving to angle: ");
        Serial.println(angle);
        lastAngle = angle;  // 마지막 각도를 저장하여 중복 실행 방지
      } else if (angle == lastAngle) {
        Serial.println("Already at this angle.");
      } else {
        Serial.println("Please enter an angle between 0 and 180.");
      }
    }
  }
}

// 각도 -> 펄스 폭 변환 함수 (1000us ~ 2000us)
int angleToPulseWidth(int angle) {
  return map(angle, 0, 180, 1000, 2000);  // 0~180도 -> 1000~2000 마이크로초 변환
}

// 서보 모터 제어 (펄스 폭을 적용하여 서보 모터를 움직임)
void moveServo(int pulseWidth) {
  // 서보 모터의 주기(20ms) 동안 HIGH와 LOW를 제어하여 PWM 신호 생성
  digitalWrite(SERVO_PIN, HIGH);  // 서보 모터 핀을 HIGH로 설정
  delayMicroseconds(pulseWidth);  // 펄스 폭 동안 대기 (1ms~2ms)
  digitalWrite(SERVO_PIN, LOW);   // 서보 모터 핀을 LOW로 설정
  delayMicroseconds(SERVO_PERIOD - pulseWidth);  // 나머지 시간 동안 LOW 유지 (20ms - 펄스 폭)
}
