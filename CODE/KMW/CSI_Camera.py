import cv2

def gstreamer_pipeline(
    sensor_id=0, capture_width=1280, capture_height=720, framerate=30, flip_method=0
):
    return (
        f"nvarguscamerasrc sensor-id={sensor_id} ! "
        f"video/x-raw(memory:NVMM), width=(int){capture_width}, height=(int){capture_height}, "
        f"format=(string)NV12, framerate=(fraction){framerate}/1 ! "
        f"nvvidconv flip-method={flip_method} ! "
        f"video/x-raw, width=(int){capture_width}, height=(int){capture_height}, format=(string)BGRx ! "
        f"videoconvert ! video/x-raw, format=(string)BGR ! appsink"
    )

def capture_camera():
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    
    if cap.isOpened():
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("CSI Camera", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        print("Can not open camera!")

    cap.release()
    cv2.destroyAllWindows()

capture_camera()
