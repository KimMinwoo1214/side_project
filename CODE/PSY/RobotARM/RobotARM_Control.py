import serial
import time

# 아두이노와의 시리얼 포트 설정
port = 'COM6'  # 자신의 포트에 맞게 수정
baudrate = 1000000
ser = serial.Serial(port, baudrate)

time.sleep(2)  # 아두이노와 연결될 때까지 잠시 대기

while True:
    try:
        # 사용자로부터 각도 입력받기

        # angle1 - 1024가 90도 / angle2 - 3072가 90도 / angle3 - 1024가 90도
        # angle1 - 3072가 270도 / angle2 - 1024가 270도 / angle3 - 3072가 270도
        angle1 = int(input("첫 번째, 두 번째 서보 각도를 입력하세요 (0-4095): ")) 
        angle2 = int(input("세 번째 서보 각도를 입력하세요 (0-4095): "))
        angle3 = int(input("네 번째 서보 각도를 입력하세요 (0-4095): "))
        
        # 입력한 각도 값을 아두이노로 전송 (,로 구분)
        ser.write(f"{angle1},{angle2},{angle3}\n".encode('utf-8'))
        
    except ValueError:
        print("잘못된 입력입니다. 정수를 입력하세요.")
    except KeyboardInterrupt:
        print("종료합니다.")
        break

ser.close()
