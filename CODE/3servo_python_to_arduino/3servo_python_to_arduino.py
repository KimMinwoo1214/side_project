import serial
import time

# 아두이노와 연결할 시리얼 포트 설정 (예: COM3 또는 /dev/ttyUSB0)
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)

def send_servo_angles(angles):
    # 아두이노에 각도 데이터를 전송
    arduino.write(f"{angles}\n".encode())
    time.sleep(0.1)  # 약간의 지연 추가

def main():
    while True:
        # 사용자 입력 받기 (예: "90, 45, 120")
        angles = input("서보 각도들을 입력하세요 (예: 90, 45, 120): ")
        
        # 올바른 형식인지 확인
        if len(angles.split(',')) == 3:
            send_servo_angles(angles)
        else:
            print("잘못된 입력입니다. '90, 45, 120' 형식으로 입력하세요.")

if __name__ == '__main__':
    main()
