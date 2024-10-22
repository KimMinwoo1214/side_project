import serial
import time

# 아두이노가 연결된 포트 설정 (예: 'COM3' 또는 '/dev/ttyUSB0')
arduino_port = 'COM6'
baud_rate = 115200

# 시리얼 포트 초기화
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # 아두이노 초기화 대기

# 각도 값을 사용자로부터 입력받기
base_angle = input("Base Angle (0-180): ")
shoulder_angle = input("Shoulder Angle (0-180): ")
upperarm_angle = input("Upperarm Angle (0-180): ")
forearm_angle = input("Forearm Angle (0-180): ")

# 입력받은 각도 값을 쉼표로 구분하여 하나의 문자열로 결합
angles = f'{base_angle},{shoulder_angle},{upperarm_angle},{forearm_angle}\n'

# 아두이노로 전송
ser.write(angles.encode())

print("Angles sent to Arduino.")

# 시리얼 포트 닫기
ser.close()
