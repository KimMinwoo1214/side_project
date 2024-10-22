import serial
import tkinter as tk

# URT-1의 포트와 보드레이트 설정
PORT = 'COM6'  # 사용 중인 포트로 변경
BAUDRATE = 10000000

# 서보 모터 각도를 URT-1으로 전송하는 함수
def set_angle(angle):
    # URT-1에 연결
    with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
        # 명령 포맷에 맞게 각도를 문자열로 변환
        command = f'#1 P{angle} T500\r\n'  # 서보 ID는 1로 가정
        ser.write(command.encode('utf-8'))  # 명령 전송

# 슬라이더의 값이 변경될 때 호출되는 함수
def on_slider_change(value):
    angle_label.config(text=f"각도: {value}")
    set_angle(int(value))  # 슬라이더 값으로 각도 설정

# GUI 설정
root = tk.Tk()
root.title("서보 모터 제어")

angle_slider = tk.Scale(root, from_=0, to=180, orient=tk.HORIZONTAL, label="서보 각도", command=on_slider_change)
angle_slider.pack()

angle_label = tk.Label(root, text="각도: 0")
angle_label.pack()

root.mainloop()
