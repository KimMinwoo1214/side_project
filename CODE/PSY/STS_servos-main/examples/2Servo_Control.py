import serial
import time

# 시리얼 포트 설정 (Arduino 연결된 포트에 맞게 수정)
ser = serial.Serial('COM9', 115200, timeout=1)  # Windows의 경우
# ser = serial.Serial('/dev/ttyUSB0', 1000000, timeout=1)  # Ubuntu의 경우

time.sleep(2)  # 시리얼 연결 안정화 대기

try:
    while True:
        # 사용자로부터 각도 입력 받기
        angle1 = input("서보 1의 각도 입력 (0~180): ")
        angle2 = input("서보 2의 각도 입력 (0~180): ")

        # 각도를 문자열로 변환하고 '\n' 추가하여 전송
        data = f"{angle1},{angle2}\n"
        ser.write(data.encode())

        print(f"보낸 데이터: {data}")

        time.sleep(1)  # 잠시 대기 후 다시 입력

except KeyboardInterrupt:
    print("종료합니다.")
    ser.close()
