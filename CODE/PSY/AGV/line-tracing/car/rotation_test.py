from pymycobot.myagv import MyAgv
import time

try:
    MA = MyAgv('/dev/ttyAMA2', 115200)
    print('MyAgv 초기화 성공')

    print('Clockwise_Rotatation Start')
    MA.clockwise_rotation(50, 2.35)
    #time.sleep(2)
    
    print('Success! Now Stop')
    MA.stop()
#    time.sleep(1)

    print('Counterclockwise_Rotation Start')
    MA.counterclockwise_rotation(50, 2.35)
    #time.sleep(2)

    print('Success! Now Stop')
    MA.stop()

    print('Finish')


except Exception as e:
    print(f"Error: {e}")
