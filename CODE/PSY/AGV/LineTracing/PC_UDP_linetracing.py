import cv2
import numpy as np
import socket

udp_ip = "172.30.1.56"  # 수신 대기
udp_port = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((udp_ip, udp_port))
buffer_size = 65507

def udp_frame_receive(sock):
    data, addr = sock.recvfrom(buffer_size)
    frame_data = data
    
    while True:
        try:
            data, _ = sock.recvfrom(buffer_size)
            frame_data += data
        except socket.timeout:
            break

    return np.frombuffer(frame_data, dtype=np.uint8), addr

while True:
    frame_data, addr = udp_frame_receive(sock)
    
    if frame_data.size > 0:
        frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)
        
        if frame is not None:
            # 화면 처리 로직 추가
            cv2.imshow("AGV Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
