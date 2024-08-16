import serial
import time

# 아두이노와 연결할 시리얼 포트 설정 (Windows: 'COMx', Linux/Mac: '/dev/ttyUSBx' 또는 '/dev/ttyACMx')
arduino = serial.Serial(port='COM7', baudrate=9600, timeout=1)

def send_angle(angle):
    if 0 <= angle <= 180:
        # 각도를 문자열로 변환하여 아두이노로 전송
        arduino.write(f"{angle}\n".encode())
        time.sleep(0.1)  # 아두이노가 데이터를 처리할 시간을 잠시 대기
        # 아두이노에서 응답을 받음
        response = arduino.readline().decode('utf-8').strip()
        print(f"아두이노 응답: {response}")
    else:
        print("각도는 0에서 180 사이여야 합니다.")

if __name__ == "__main__":
    while True:
        try:
            angle = int(input("보낼 각도를 입력하세요 (0-180): "))
            send_angle(angle)
        except ValueError:
            print("유효한 숫자를 입력하세요.")