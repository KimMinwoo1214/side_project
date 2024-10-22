import tkinter as tk
from tkinter import messagebox

class Serial_rw:
    def __init__(self, ID):
        self.ID = ID
        # 여기에 Serial 통신 초기화 코드를 추가하세요.

    def send(self, int_arr):
        # 여기에 데이터를 서보 모터로 전송하는 코드를 추가하세요.
        print(f"Sending to ID {self.ID}: {int_arr}")

    def get_data(self, read_arr):
        # 여기에 서보 모터에서 데이터를 받는 코드를 추가하세요.
        return "00 00 00 00 00 00 00 00"  # 예시 데이터

class RAError(Exception):
    pass

class Servo():
    def __init__(self, ID, qty=1):
        self.srw = Serial_rw(ID)
        self.ID = ID
        self.pos = None
        self.speed = 0
        self.pos_ctr = 0
        self.qty = qty if ID == 254 else None

        self.read_goal_pos = 0
        self.read_pres_pos = 0
        self.read_pos_ctr = 0
        self.virtual_pos_ctr = 0
        self.read_pos_ctr_offset = 0
        self.read_move_status = 0
        self.read_work_mode = None
        self.read_max_pos_lmt = None
        self.read_curr_speed = None

        self.READ_CMD = 0x02
        self.WRITE_CMD = 0x03
        self.MAX_POS_LMT = 0xB
        self.WORK_MODE = 0x21
        self.GOAL_POS = 0x2A
        self.SPEED = 0x2E
        self.CURR_POS = 0x38
        self.MOVE_STATUS = 0x42
        self.POS_COUNTER = 0x43

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def sint2pos(self, signed_int: int):
        if signed_int < 0:
            signed_int = abs(signed_int) + 0x8000
        return signed_int

    def pos2sint(self, unsigned_int: int):
        if unsigned_int > 0x8000:
            unsigned_int = 0x8000 - unsigned_int
        return unsigned_int

    def servo_pos(self, pos):
        pos = round(self.clamp(pos, -360*8, 360*8)/360*4095)
        self.pos = self.sint2pos(pos)
        int_arr = [0xFF, 0xFF, self.ID, 5, self.WRITE_CMD,
                   self.GOAL_POS, self.pos % 256, self.pos >> 8, 0x00]
        self.srw.send(int_arr)

class ServoControllerApp:
    def __init__(self, master):
        self.master = master
        master.title("Servo Motor Controller")

        self.servos = {}
        self.servo_count = 2  # 모터의 개수 설정
        for i in range(self.servo_count):
            servo_id = i + 1
            self.servos[servo_id] = Servo(servo_id)

            label = tk.Label(master, text=f"Servo {servo_id} Angle:")
            label.grid(row=i, column=0)

            angle_entry = tk.Entry(master)
            angle_entry.grid(row=i, column=1)
            angle_entry.insert(0, "0")

            set_button = tk.Button(master, text="Set Angle", command=lambda id=servo_id, entry=angle_entry: self.set_angle(id, entry))
            set_button.grid(row=i, column=2)

    def set_angle(self, servo_id, entry):
        try:
            angle = int(entry.get())
            if angle < -360 or angle > 360:
                raise ValueError("Angle must be between -360 and 360 degrees.")
            self.servos[servo_id].servo_pos(angle)
            messagebox.showinfo("Success", f"Servo {servo_id} set to {angle} degrees.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ServoControllerApp(root)
    root.mainloop()
