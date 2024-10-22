import cv2
import socket

# 카메라 초기화
cap = cv2.VideoCapture(0)  # AGV의 카메라 장치
udp_ip = "172.30.1.56"
udp_port = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
MAX_DGRAM = 65507  # UDP 패킷 크기 제한

def udp_frame_send(sock, frame, addr):
    encoded, buffer = cv2.imencode('.jpg', frame)
    data = buffer.tobytes()

    # 데이터를 쪼개서 전송
    for i in range(0, len(data), MAX_DGRAM):
        sock.sendto(data[i:i+MAX_DGRAM], addr)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    udp_frame_send(sock, frame, (udp_ip, udp_port))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
