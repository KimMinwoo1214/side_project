import serial
import time

# URT-1의 포트와 보드레이트 설정
PORT = 'COM6'  # 사용 중인 포트로 변경
BAUDRATE = 1000000

def scan_servo_id():
    with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
        found_ids = []  # 찾은 ID를 저장할 리스트

        for servo_id in range(0, 254):  # 일반적으로 ID는 1에서 255 사이
            # ID 설정 명령
            command = f'#{servo_id} P0 T500\r\n'  # 각도 0으로 설정
            ser.write(command.encode('utf-8'))
            time.sleep(0.1)  # 응답 시간을 주기 위해 잠시 대기

            # 응답 읽기
            if ser.in_waiting > 0:
                response = ser.read(ser.in_waiting).decode('utf-8').strip()
                if response:
                    found_ids.append(servo_id)  # 찾은 ID 추가
                    print(f'서보 ID {servo_id}: {response}')

        if not found_ids:
            print("서보 ID를 찾지 못했습니다.")
        else:
            print("찾은 서보 ID:", found_ids)

# 스캐닝 시작
scan_servo_id()
