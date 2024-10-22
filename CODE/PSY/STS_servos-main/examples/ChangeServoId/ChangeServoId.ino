#include <SCServo.h>

// 서보 모터 객체 생성
SCS sc;

void setup() {
    Serial.begin(115200);  // 시리얼 통신 시작
    sc.begin(1000000);      // 서보 모터 초기화
}

void loop() {
    if (Serial.available() > 0) {
        String data = Serial.readStringUntil('\n');  // 데이터 수신
        int commaIndex = data.indexOf(',');
        
        if (commaIndex != -1) {
            int angle1 = data.substring(0, commaIndex).toInt();  // 첫 번째 각도
            int angle2 = data.substring(commaIndex + 1).toInt();  // 두 번째 각도
            
            // 각도 설정 (여기서 ID는 예시입니다. 실제 ID에 맞게 수정하세요.)
            sc.WritePos(2, angle1, 2, 1500);  // 서보 1 설정
            sc.WritePos(3, angle2, 2, 1500);  // 서보 2 설정
        }
    }
}
