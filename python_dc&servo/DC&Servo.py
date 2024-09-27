import serial
import time

# 시리얼 포트와 통신 속도 설정 (포트는 환경에 따라 다를 수 있음)
ser = serial.Serial('COM6', 9600)  # COM 포트 번호는 사용 환경에 맞게 설정하세요
time.sleep(2)  # 시리얼 통신 안정화를 위해 잠시 대기

def send_command(dc_command, dc_speed, servo_angle):
    # DC 모터 명령어와 속도 전송
    ser.write(f"{dc_command}{dc_speed}\n".encode())
    print(f"DC 모터 명령어: {dc_command}, 속도: {dc_speed} 전송")
    
    # 서보 모터 각도 전송
    ser.write(f"A{servo_angle}\n".encode())
    print(f"서보 모터 각도: {servo_angle} 전송")

print("명령어를 입력하세요 (예: G100, A90). 두 개의 명령어를 연속으로 입력하세요.")

while True:
    # DC 모터 명령어 입력 (G, B, S)와 속도 값 입력
    dc_input = input("DC 모터 명령어 (예: G100): ")
    # 서보 모터 각도 입력 (0~180도)
    servo_input = input("서보 모터 각도 (0~180도): ")

    if len(dc_input) > 1 and len(servo_input) > 1:
        dc_command = dc_input[0].upper()  # DC 모터 명령어 추출 (G, B, S)
        try:
            dc_speed = int(dc_input[1:])  # DC 모터 속도 값 추출 (숫자로 변환)
            servo_angle = int(servo_input)  # 서보 모터 각도 값 추출 (숫자로 변환)
            
            if dc_command in ['G', 'B', 'S']:
                if 0 <= dc_speed <= 250:
                    if 70 <= servo_angle <= 110:
                        send_command(dc_command, dc_speed, servo_angle)
                    else:
                        print("서보 모터 각도는 70에서 110 사이의 값이어야 합니다.")
                else:
                    print("DC 모터 속도는 0에서 250 사이의 값이어야 합니다.")
            else:
                print("잘못된 DC 모터 명령어입니다. G, B, S 중 하나를 입력하세요.")
        except ValueError:
            print("값은 숫자로 입력하세요.")
    else:
        print("명령어와 값을 함께 입력하세요.")