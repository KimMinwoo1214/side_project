from pymycobot.myagv import MyAgv
import time

MA = MyAgv('/dev/ttyAMA2', 115200)

#MA.go_ahead(10)
#time.sleep(1)

MA.stop()
time.sleep(1)
a = int(input("Type speed of rotation: "))

while True:
    # a = int(input("Type 0 if you want to stop: "))
    
    if a != 0:
        MA.clockwise_rotation(a)
        a = int(input("Type 0 if you want to stop: "))
    
    elif a == 0:
        break

#time.sleep(0.5)
MA.stop()

