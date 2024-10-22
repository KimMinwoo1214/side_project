import serial
import time
import threading

HEADER = 0xFE

def send_wheel_command(port, direction_1, direction_2, direction_3):
    command = [
        HEADER,
        HEADER,
        direction_1,
        direction_2,
        direction_3,
        (direction_1 + direction_2 + direction_3) & 0xFF  # 체크섬
    ]
    port.write(bytearray(command))
    port.flush()

def move_robot(port):
    global direction_1, direction_2, direction_3, state

    while True:
        send_wheel_command(port, direction_1, direction_2, direction_3)
        time.sleep(0.1)  # 주기적으로 명령 전송

def handle_input():
    global direction_1, direction_2, direction_3, state

    while True:
        input("Press Enter to change direction (or type 'exit' to quit): ")
        if state == "moving_forward":
            direction_1, direction_2, direction_3 = 128, 128, 128  # 멈춤
            state = "panning_left"  # 상태 변경
            print("Robot stopped, now panning left...")
        elif state == "panning_left":
            direction_1, direction_2 = 128, 128 - 50  # 반시계 방향 회전
            state = "panning_right"  # 상태 변경
            print("Robot panning left...")
        elif state == "panning_right":
            direction_1, direction_2 = 128, 128 + 50  # 시계 방향 회전
            state = "moving_forward"  # 다시 앞으로 이동
            print("Robot panning right...")

def main():
    global direction_1, direction_2, direction_3, state

    port = serial.Serial(port="/dev/ttyAMA2", baudrate=115200, timeout=0.1)
    time.sleep(2)  # 포트 안정화 대기

    direction_1, direction_2, direction_3 = 128, 128, 128  # 기본 정지 상태
    state = "moving_forward"  # 초기 상태

    move_thread = threading.Thread(target=move_robot, args=(port,))
    input_thread = threading.Thread(target=handle_input)

    move_thread.start()
    input_thread.start()

    input_thread.join()  # 입력 스레드가 종료될 때까지 대기
    send_wheel_command(port, 128, 128, 128)  # 정지
    move_thread.join()  # 이동 스레드 종료 대기

    port.close()  # 포트 닫기

if __name__ == "__main__":
    main()
