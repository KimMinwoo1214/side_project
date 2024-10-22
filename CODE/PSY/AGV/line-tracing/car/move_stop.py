import time
import threading
from pymycobot.myagv import MyAgv

# AGV 초기화
try:
    MA = MyAgv('/dev/ttyAMA2', 115200)
    print("MyAgv 초기화 성공")
except Exception as e:
    print(f"AGV 초기화 실패: {e}")
    exit()

# 사용자 입력에 따른 AGV 제어 함수
def control_agv():
    global stop_flag, current_thread
    while True:
        command = input("w: 앞으로, a: 반시계 회전, d: 시계 회전, s: 정지 -> ")
        if command.lower() == 'w':
            try:
                stop_flag = True
                if current_thread is not None and current_thread.is_alive():
                    current_thread.join()
                stop_flag = False
                current_thread = threading.Thread(target=move_with_stop, args=(MA.go_ahead, 1, 10))
                current_thread.start()
                print("AGV 앞으로 이동")
            except Exception as e:
                print(f"앞으로 이동 명령 에러: {e}")
        elif command.lower() == 'd':
            try:
                stop_flag = True
                if current_thread is not None and current_thread.is_alive():
                    current_thread.join()
                stop_flag = False
                current_thread = threading.Thread(target=move_with_stop, args=(MA.clockwise_rotation, 1, 10))
                current_thread.start()
                print("AGV 시계방향 회전")
            except Exception as e:
                print(f"시계방향 회전 명령 에러: {e}")
        elif command.lower() == 'a':
            try:
                stop_flag = True
                if current_thread is not None and current_thread.is_alive():
                    current_thread.join()
                stop_flag = False
                current_thread = threading.Thread(target=move_with_stop, args=(MA.counterclockwise_rotation, 1, 10))
                current_thread.start()
                print("AGV 반시계방향 회전")
            except Exception as e:
                print(f"반시계방향 회전 명령 에러: {e}")
        elif command.lower() == 's':
            try:
                stop_flag = True
                if current_thread is not None and current_thread.is_alive():
                    current_thread.join()
                MA.stop()  # 정지
                print("AGV 정지")
            except Exception as e:
                print(f"정지 명령 에러: {e}")
        else:
            print("알 수 없는 명령입니다. 다시 입력해주세요.")

        # 사용자 입력에 따라 새로운 명령이 오면 동작 재개
        time.sleep(0.1)  # 짧은 대기 시간 설정

# 이동 중 강제 정지를 처리하는 함수
def move_with_stop(move_function, duration, speed):
    start_time = time.time()
    while not stop_flag and (time.time() - start_time < duration):
        move_function(speed, duration)
        time.sleep(0.1)

# 초기 상태 설정
stop_flag = False
current_thread = None

# AGV 제어 시작
control_thread = threading.Thread(target=control_agv)
control_thread.start()

# 메인 스레드에서 모든 동작이 끝날 때까지 대기
control_thread.join()
