import serial
import time

# 아두이노와 연결할 시리얼 포트 설정 (예: 'COM3' 또는 '/dev/ttyACM0')
arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)

def set_servo_angle():
    while True:
        try:
            angle = int(input("서보모터의 각도를 입력하세요 (0-180): "))
            if 0 <= angle <= 180:
                arduino.write(f"{angle}\n".encode())  # 각도를 시리얼로 전송
                print(f"전송된 각도: {angle}")
            else:
                print("각도는 0에서 180 사이여야 합니다.")
        except ValueError:
            print("유효한 숫자를 입력하세요.")
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            break

    arduino.close()  # 시리얼 포트 닫기

# 함수 실행
set_servo_angle()
