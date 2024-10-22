from serial_servo import *
import time


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

        move3svo(0, svo_speed)
        svo_speed += 250
        read_all_motor_info()
        move3svo(90, svo_speed)
        svo_speed += 250
        read_all_motor_info()
        move3svo(180, svo_speed)
        svo_speed += 250
        read_all_motor_info()
        move3svo(270, svo_speed)
        svo_speed += 250
        read_all_motor_info()
        move3svo(360, svo_speed)
        svo_speed += 250
        read_all_motor_info()
        if svo_speed > 3500:
            svo_speed = 0


if __name__ == '__main__':
    svo1 = Servo(1)
    svo2 = Servo(2)
    svo3 = Servo(3)
    svo_all = Servo(254)
    initial_setup()
    main()
