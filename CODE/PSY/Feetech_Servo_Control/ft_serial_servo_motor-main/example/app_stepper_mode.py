# Example for stepper servo mode
import os
import sys

# Append parent directory to import path, import file from parent directory
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(__file__)  # ./file.py
print(os.path.abspath(__file__))  # ./file.py
print(os.path.dirname(os.path.abspath(__file__)))  # ./
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # ../

import time
from serial_servo import *

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


def change_mode_3():
    initial_setup()
    svo_all.servo_pos_spd(0, 0)
    while svo1.isMoving() and svo2.isMoving() and svo3.isMoving():
        continue
    svo1.change_mod(3)
    svo2.change_mod(3)
    svo3.change_mod(3)


def read_all_motor_info():
    svo1.read_all_info()
    svo2.read_all_info()
    svo3.read_all_info()


def main():
    svo_speed = 0

    move3svo(360*4, svo_speed)
    read_all_motor_info()
    print("===================================")
    time.sleep(2)

    move3svo(360*4, svo_speed)
    read_all_motor_info()
    print("===================================")
    time.sleep(2)

    move3svo(-360*8, svo_speed)
    read_all_motor_info()
    print("===================================")


if __name__ == '__main__':
    svo1 = Servo(1)
    svo2 = Servo(2)
    svo3 = Servo(3)
    svo_all = Servo(254,3)
    change_mode_3()
    # svo1.setSpeed(300)
    main()
