# Example for publish same command to all motor
import os
import sys
# Append parent directory to import path, import file from parent directory
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(__file__) #./file.py
print(os.path.abspath(__file__)) #./file.py
print(os.path.dirname(os.path.abspath(__file__))) #./
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #../

from serial_servo import *
import time

def timer(delay):
    start_time = time.time()
    time_diff = 0
    while time_diff < delay:
        a, b, c = svo1.ser.read_mv_status()
        print("read_goal_pos = ", a, "read_pres_pos = ",
              b, "read_move_status = ", c)
        time_diff = time.time() - start_time


def move3svo(pos, svo_speed):
    svo1.servo_pos_spd(pos, svo_speed)
    svo2.servo_pos_spd(pos, svo_speed)
    svo3.servo_pos_spd(pos, svo_speed)
    while svo1.isMoving() and svo2.isMoving() and svo3.isMoving():
        continue


def initial_setup():
    svo1.change_mod(0)
    svo2.change_mod(0)
    svo3.change_mod(0)


def change_mode3():
    svo1.change_mod(3)
    svo2.change_mod(3)
    svo3.change_mod(3)


def read_all_motor_info():
    svo1.read_all_info()
    svo2.read_all_info()
    svo3.read_all_info()


def main():
    svo_speed = 0
    while (True):

        svo_all.servo_pos_spd(0, svo_speed)
        while svo1.isMoving() and svo2.isMoving() and svo3.isMoving():
            continue
        svo_speed += 250
        read_all_motor_info()

        svo_all.servo_pos_spd(90, svo_speed)
        while svo1.isMoving() and svo2.isMoving() and svo3.isMoving():
            continue
        svo_speed += 250
        read_all_motor_info()

        svo_all.servo_pos_spd(180, svo_speed)
        while svo1.isMoving() and svo2.isMoving() and svo3.isMoving():
            continue
        svo_speed += 250
        read_all_motor_info()

        svo_all.servo_pos_spd(270, svo_speed)
        while svo1.isMoving() and svo2.isMoving() and svo3.isMoving():
            continue
        svo_speed += 250
        read_all_motor_info()

        svo_all.servo_pos_spd(360, svo_speed)
        while svo1.isMoving() and svo2.isMoving() and svo3.isMoving():
            continue
        svo_speed += 250
        read_all_motor_info()

        if svo_speed > 3500:
            svo_speed = 0
        svo_speed += 250
        if svo_speed > 3500:
            svo_speed = 0


if __name__ == '__main__':
    svo1 = Servo(1)
    svo2 = Servo(2)
    svo3 = Servo(3)
    svo_all = Servo(254)
    initial_setup()
    main()
