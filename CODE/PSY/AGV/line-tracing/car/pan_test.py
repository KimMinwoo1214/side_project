from pymycobot.myagv import MyAgv
import time

MA = MyAgv('/dev/ttyAMA2', 115200)

MA.pan_left(10)
time.sleep(0.5)

MA.stop()

MA.pan_right(10)
time.sleep(0.5)

MA.stop()
