import cv2
import numpy as np
import math

# 카메라 장치 설정
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# 노란색 HSV 범위 설정
h_min, h_max = 20, 30
s_min, s_max = 100, 255
v_min, v_max = 100, 255

previous_line = None

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting...")
        break

    # BGR에서 HSV로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # HSV 범위를 설정하여 마스크 생성
    lower_bound = np.array([h_min, s_min, v_min])
    upper_bound = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # 마스크의 윤곽선 찾기
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 가장 큰 윤곽선 선택 (잡음 제거를 위해)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M['m00'] > 0:
            # 무게중심 계산
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            # 무게중심에 원 그리기
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # 이전 무게중심이 있는 경우, 현재 중심과 이전 중심을 연결하는 선 그리기
            if previous_line is not None:
                prev_cx, prev_cy = previous_line
                cv2.line(frame, (prev_cx, prev_cy), (cx, cy), (0, 255, 0), 2)

                # 각도 계산
                dx = cx - prev_cx
                dy = cy - prev_cy
                angle = math.degrees(math.atan2(dy, dx))

                # 각도에 따라 방향 결정
                if -10 <= angle <= 10 or 170 <= angle <= 180 or -180 <= angle <= -170:
                    direction = "Go"
                elif angle < -10:
                    direction = "Left"
                else:
                    direction = "Right"

                # 방향 출력
                cv2.putText(frame, f"Direction: {direction} ({angle:.2f} degrees)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # 현재 무게중심을 이전 무게중심으로 설정
            previous_line = (cx, cy)

    # 결과 표시
    result = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('Original', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Filtered', result)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
