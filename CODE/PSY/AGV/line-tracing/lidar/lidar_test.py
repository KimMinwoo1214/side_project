import serial
import struct
import math
import RPi.GPIO as GPIO
import time

# 설정
MOTOR_PIN = 20
port = "/dev/ttyAMA0"  # 적절한 포트로 수정 필요
baudrate = 115200

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

def parse_lidar_data(data):
    # 데이터를 적절히 슬라이싱하고 파싱합니다
    header = data[:10]  # 예시로 헤더 추출
    payload = data[10:]  # 나머지 데이터를 페이로드로 설정
    
    distances = []
    for i in range(0, len(payload), 5):  # 각 데이터는 5바이트라고 가정
        if i + 5 <= len(payload):
            point_data = payload[i:i+5]
            distance, intensity = struct.unpack('<H', point_data[:2])[0], point_data[2]
            distances.append((distance, intensity))
    
    return distances

def convert_to_cartesian(distances):
    cartesian_points = []
    angle_increment = 1.0  # 각 데이터 포인트 간의 각도 증가 값 (도 단위)
    current_angle = 0.0

    for distance, intensity in distances:
        # 극 좌표를 직교 좌표로 변환
        x = distance * math.cos(math.radians(current_angle))
        y = distance * math.sin(math.radians(current_angle))
        cartesian_points.append((x, y, intensity))
        
        # 각도를 증가시킵니다
        current_angle += angle_increment
    
    return cartesian_points

try:
    # 모터 켜기
    GPIO.output(MOTOR_PIN, GPIO.HIGH)
    print("LiDAR motor ON")
    time.sleep(5)  # LiDAR가 시작될 시간을 충분히 제공 (5초 대기)

    # LiDAR 연결 설정
    ser = serial.Serial(
        port,
        baudrate,
        timeout=1,
        rtscts=True,
        dsrdtr=True,
        xonxoff=False
    )
    print(f"Connected to YDLIDAR on {port}")

    # LiDAR 데이터 읽기
    while True:
        data = ser.readline()  # readline() 사용하여 데이터 읽기
        if data:
            print(f"Received raw data: {data}")
            distances = parse_lidar_data(data)
            cartesian_points = convert_to_cartesian(distances)
            
            # 변환된 데이터를 출력
            for point in cartesian_points:
                print(f"x: {point[0]}, y: {point[1]}, intensity: {point[2]}")

except serial.SerialException as e:
    print(f"Error: {e}")

except KeyboardInterrupt:
    print("Stopping LiDAR and motor...")

finally:
    # 모터 끄기
    GPIO.output(MOTOR_PIN, GPIO.LOW)
    GPIO.cleanup()
    if ser.is_open:
        ser.close()
    print("LiDAR motor OFF and GPIO cleaned up")
