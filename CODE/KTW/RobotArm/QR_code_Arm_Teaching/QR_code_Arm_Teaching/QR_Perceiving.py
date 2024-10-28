import cv2
from pyzbar import pyzbar

# 인식할 QR 코드의 데이터 정의 (실제 QR 코드 데이터로 변경하세요)
QR_CODES = {
    "QR_CODE_DATA_1": "첫 번째 QR 코드가 인식되었습니다!",
    "QR_CODE_DATA_2": "두 번째 QR 코드가 인식되었습니다!",
    "QR_CODE_DATA_3": "세 번째 QR 코드가 인식되었습니다!",
    "QR_CODE_DATA_4": "네 번째 QR 코드가 인식되었습니다!",
}

def decode_qr(frame):
    # 프레임에서 QR 코드 디코딩
    decoded_objects = pyzbar.decode(frame)
    for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8')
        if qr_data in QR_CODES:
            print(QR_CODES[qr_data])
            # 추가 동작을 여기에 구현할 수 있습니다.
        else:
            print(f"알 수 없는 QR 코드 데이터: {qr_data}")
        # QR 코드 주변에 사각형 그리기
        (x, y, w, h) = obj.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # QR 코드 데이터 표시
        cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
    return frame

def main():
    # 웹캠 초기화 (기본 카메라 사용, 다른 카메라를 사용하려면 인덱스 변경)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("웹캠을 열 수 없습니다.")
        return

    print("QR 코드 스캐너가 실행 중입니다. 'q' 키를 눌러 종료하세요.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 가져올 수 없습니다.")
            break

        # QR 코드 디코딩 및 표시
        frame = decode_qr(frame)

        # 결과 프레임 보여주기
        cv2.imshow('QR 코드 스캐너', frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 자원 해제
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()