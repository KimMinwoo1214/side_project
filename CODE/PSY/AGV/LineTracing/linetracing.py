import cv2
import numpy as np
import math

def calculate_yellow_line_angle_live():
    # 카메라 캡처 시작 (0은 기본 카메라)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 가져올 수 없습니다.")
            break

        # 이미지 복사
        output = frame.copy()
        height, width = frame.shape[:2]
        center_y = height // 2

        # 중앙 분할 선 그리기 (파란색, 두께 2)
        cv2.line(output, (0, center_y), (width, center_y), (255, 0, 0), 2)

        # BGR에서 HSV로 변환
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Gaussian Blur 적용 (노이즈 감소)
        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

        # 노란색 범위 설정 (HSV)
        lower_yellow = np.array([20, 125, 125])  # Hue 범위를 좁힘
        upper_yellow = np.array([30, 255, 255])  # 좁혀진 Hue 범위

        # 노란색 마스크 생성
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # 노이즈 제거 (형태학적 연산)
        kernel = np.ones((5, 5), np.uint8)  # 커널 크기 확대
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

        # 얇은 라인을 강화하기 위해 다이레이션 적용
        mask = cv2.dilate(mask, kernel, iterations=1)

        # 에지 검출 (Canny)
        edges = cv2.Canny(mask, 50, 200, apertureSize=3)  # 상한값을 약간 높임

        # 허프 변환을 이용한 선 검출
        lines = cv2.HoughLinesP(edges, 1, math.pi/180, threshold=30, minLineLength=30, maxLineGap=10)

        detected = False  # 선이 하나라도 검출되었는지 확인하는 플래그

        if lines is not None:
            # 가장 긴 선을 선택하기 위해 길이를 계산하여 정렬
            lines = sorted(lines, key=lambda line: math.hypot(line[0][2] - line[0][0], line[0][3] - line[0][1]), reverse=True)
            for line in lines:
                x1, y1, x2, y2 = line[0]
                
                # 선이 중앙 분할 선과 교차하는지 확인
                if (y1 < center_y and y2 > center_y) or (y1 > center_y and y2 < center_y):
                    # 선 그리기 (녹색, 두께 2)
                    cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # 각도 계산
                    angle_rad = math.atan2(y2 - y1, x2 - x1)
                    angle_deg = math.degrees(angle_rad)

                    # 각도 출력
                    print(f"검출된 선의 각도: {angle_deg:.2f}도")

                    # 각도에 따른 메시지 출력
                    if (-90 <= angle_deg <= -80) or (80 <= angle_deg <= 90):
                        direction = "Go"
                    elif (0 <= angle_deg < 80):
                        direction = "Right"
                    elif (-80 <= angle_deg < 0):
                        direction = "Left"
                    else:
                        direction = "Unknown"

                    print(direction)

                    # 각도 표시
                    if y2 != y1:
                        t = (center_y - y1) / (y2 - y1)
                        intersect_x = int(x1 + t * (x2 - x1))
                        intersect_y = center_y
                        cv2.circle(output, (intersect_x, intersect_y), 5, (0, 0, 255), -1)
                        cv2.putText(output, f"{angle_deg:.2f} deg", (intersect_x + 10, intersect_y - 10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)  # 텍스트 색상 변경
                        # 메시지 표시
                        cv2.putText(output, direction, (intersect_x + 10, intersect_y + 20), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)  # 텍스트 색상 변경
                    
                    detected = True  # 선이 검출되었음을 표시
                    break  # 첫 번째 교차 선만 처리
            if not detected:
                print("중앙 선과 교차하는 노란색 선을 찾을 수 없습니다.")
        else:
            print("노란색 선을 찾을 수 없습니다.")

        # 결과 이미지 표시
        cv2.imshow('Yellow Line Detection Live', output)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 자원 해제
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    calculate_yellow_line_angle_live()