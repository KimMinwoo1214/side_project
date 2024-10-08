import cv2, imutils, socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_ip = '172.30.1.100'
port = 9999
message = b'Hello'

client_socket.sendto(message, (host_ip, port))
fps, st, frames_to_count, cnt = (0, 0, 20, 0)

while True:
    packet, _ = client_socket.recvfrom(BUFF_SIZE)
    data = base64.b64decode(packet, ' /')
    npdata = np.frombuffer(data, dtype=np.uint8)  # fromstring -> frombuffer 변경
    frame = cv2.imdecode(npdata, 1)

    if frame is not None:  # 프레임이 제대로 수신되었는지 확인
        frame_cvt = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_mask1 = cv2.inRange(frame_cvt, np.array([0, 100, 100]), np.array([20, 255, 255]))
        frame_mask2 = cv2.inRange(frame_cvt, np.array([160, 100, 100]), np.array([180, 255, 255]))
        frame_mask = frame_mask1 + frame_mask2
        cont_list, hierachy = cv2.findContours(frame_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        try:
            c = max(cont_list, key=cv2.contourArea)
            M = cv2.moments(c)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            img_con = cv2.drawContours(frame, c, -1, (0, 0, 255), 1)
            image = cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
        except:
            pass

        frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("RECEIVING VIDEO", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            client_socket.close()
            cv2.destroyAllWindows()
            break
        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count / (time.time() - st))
                st = time.time()
                cnt = 0
            except:
                pass
        cnt += 1
    else:
        print("Frame not received")
