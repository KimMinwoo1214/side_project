import cv2
import numpy as np

def nothing(x):
    pass

# 카메라 장치 설정
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# 윈도우 생성
cv2.namedWindow('HSV Adjustments')

# 트랙바 생성
cv2.createTrackbar('H_min', 'HSV Adjustments', 0, 179, nothing)
cv2.createTrackbar('H_max', 'HSV Adjustments', 179, 179, nothing)
cv2.createTrackbar('S_min', 'HSV Adjustments', 0, 255, nothing)
cv2.createTrackbar('S_max', 'HSV Adjustments', 255, 255, nothing)
cv2.createTrackbar('V_min', 'HSV Adjustments', 0, 255, nothing)
cv2.createTrackbar('V_max', 'HSV Adjustments', 255, 255, nothing)

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting...")
        break

    # BGR에서 HSV로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 트랙바에서 HSV 값 가져오기
    h_min = cv2.getTrackbarPos('H_min', 'HSV Adjustments')
    h_max = cv2.getTrackbarPos('H_max', 'HSV Adjustments')
    s_min = cv2.getTrackbarPos('S_min', 'HSV Adjustments')
    s_max = cv2.getTrackbarPos('S_max', 'HSV Adjustments')
    v_min = cv2.getTrackbarPos('V_min', 'HSV Adjustments')
    v_max = cv2.getTrackbarPos('V_max', 'HSV Adjustments')

    # HSV 범위를 설정하여 마스크 생성
    lower_bound = np.array([h_min, s_min, v_min])
    upper_bound = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # 원본 프레임과 마스크를 AND 연산하여 특정 색상만 추출
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # 결과 표시
    cv2.imshow('Original', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Filtered', result)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()

