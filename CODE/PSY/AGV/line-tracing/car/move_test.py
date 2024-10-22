from pymycobot.myagv import MyAgv
import time

try:
    MA = MyAgv('/dev/ttyAMA2', 115200)
    print("MyAgv 초기화 성공")
    
    MA.retreat(10, 1.3)
    print("Back")
    
    time.sleep(1)

    # 앞으로 이동 명령 전송 및 응답 확인
    print("앞으로 이동 명령 전송")
    MA.go_ahead(10, 1.35)
    #time.sleep(2)
    
    #MA.go_ahead(5, 1)
    # 정지 명령 전송 및 응답 확인
    print("정지 명령 전송")
    MA.stop()
    
    #print("후진 명령 전송")
    #MA.retreat(10, 1.5)
    #time.sleep(2)

    #print("정지 명령 전송")
    #MA.stop()
#    print("좌측 이동")
#    MA.pan_left(50)
#    time.sleep(2)
    
#    print("정지")
#    MA.stop()

#    print("우측 이동")
#    MA.pan_right(50)
#    time.sleep(2)

#   print("정지")
#    MA.stop()

except Exception as e:
    print(f"에러 발생: {e}")

