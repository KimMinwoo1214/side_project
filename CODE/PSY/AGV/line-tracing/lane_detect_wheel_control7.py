import cv2
import numpy as np
import math
import serial
import time
import threading

# Global variables for wheel directions and state
direction_1, direction_2, direction_3 = 128, 128, 128  # Default stop
state = "stopped"
HEADER = 0xFE

# New global variables for rotation sequences
rotation_sequence = None  # None, 'cw', 'ccw'
sequence_state = None     # 'forward', 'rotating'
sequence_start_time = 0

def send_wheel_command(port, direction_1, direction_2, direction_3):
    """
    Send wheel command to the AGV via serial port.
    """
    command = [
        HEADER,
        HEADER,
        direction_1,
        direction_2,
        direction_3,
        (direction_1 + direction_2 + direction_3) & 0xFF  # Checksum
    ]
    try:
        port.write(bytearray(command))
        port.flush()
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")

def move_robot(port):
    """
    Thread function to continuously send wheel commands based on global direction variables.
    """
    global direction_1, direction_2, direction_3, state
    while True:
        send_wheel_command(port, direction_1, direction_2, direction_3)
        time.sleep(0.1)  # Send command every 100ms

def calculate_yellow_line_angle_live():
    """
    Capture video from the camera, detect yellow lines, determine direction, and update wheel commands.
    """
    global direction_1, direction_2, direction_3, state
    global rotation_sequence, sequence_state, sequence_start_time

    # Start camera capture (0 is the default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Cannot receive frame.")
            break

        # Copy the frame for output
        output = frame.copy()
        height, width = frame.shape[:2]
        center_y = int(height * 0.7)

        # Draw center dividing line (Blue, thickness 2)
        cv2.line(output, (0, center_y), (width, center_y), (255, 0, 0), 2)

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Apply Gaussian Blur to reduce noise
        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

        # Define yellow color range in HSV
        lower_yellow = np.array([15, 100, 100])
        upper_yellow = np.array([35, 255, 255])

        # Create yellow mask
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Remove noise using morphological operations
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

        # Dilate to strengthen lines
        mask = cv2.dilate(mask, kernel, iterations=1)

        # Edge detection using Canny
        edges = cv2.Canny(mask, 50, 200, apertureSize=3)

        # Hough Transform to detect lines
        lines = cv2.HoughLinesP(edges, 1, math.pi/180, threshold=30, minLineLength=30, maxLineGap=10)

        detected = False  # Flag to check if any line is detected

        current_time = time.time()

        # Handle rotation sequences if in progress
        if rotation_sequence is not None:
            if sequence_state == "forward":
                if current_time - sequence_start_time >= 1.5:
                    # Transition to rotating state
                    sequence_state = "rotating"
                    sequence_start_time = current_time
                    if rotation_sequence == "cw":
                        # Set directions for clockwise rotation
                        direction_1, direction_2, direction_3 = 128, 128, 126  # Adjust as needed for rotation
                        state = "rotating_clockwise"
                        print("Starting clockwise rotation.")
                    elif rotation_sequence == "ccw":
                        # Set directions for counterclockwise rotation
                        direction_1, direction_2, direction_3 = 128, 128, 130  # Adjust as needed for rotation
                        state = "rotating_counterclockwise"
                        print("Starting counterclockwise rotation.")
            elif sequence_state == "rotating":
                if current_time - sequence_start_time >= 3.0:
                    # Rotation completed, stop
                    direction_1, direction_2, direction_3 = 128, 128, 128  # Stop
                    state = "stopped"
                    print(f"{rotation_sequence.upper()} rotation completed. Stopping.")
                    rotation_sequence = None
                    sequence_state = None
            # During rotation sequence, skip processing new lines
        else:
            # Only process new lines if not in a rotation sequence
            if lines is not None:
                # Sort lines by length in descending order
                lines = sorted(lines, key=lambda line: math.hypot(line[0][2] - line[0][0], line[0][3] - line[0][1]), reverse=True)
                for line in lines:
                    x1, y1, x2, y2 = line[0]

                    # Check if the line crosses the center dividing line
                    if (y1 < center_y and y2 > center_y) or (y1 > center_y and y2 < center_y):
                        # Draw the detected line (Green, thickness 2)
                        cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 2)

                        # Calculate the angle of the line
                        angle_rad = math.atan2(y2 - y1, x2 - x1)
                        angle_deg = math.degrees(angle_rad)

                        # Print the detected angle
                        print(f"Detected line angle: {angle_deg:.2f} degrees")

                        # Determine direction based on angle
                        if (-90 <= angle_deg <= -45) or (45 <= angle_deg <= 90):
                            direction = "f"  # Forward
                        elif (0 <= angle_deg < 45):
                            direction = "ccw"  # Clockwise
                        elif (-45 <= angle_deg < 0):
                            direction = "cw"  # Counterclockwise
                        else:
                            direction = "Unknown"

                        print(f"Direction: {direction}")

                        # Update wheel commands based on direction
                        if direction == "f":
                            direction_1, direction_2, direction_3 = 128 + 5, 128, 128  # Move forward
                            state = "moving_forward"
                        elif direction == "cw":
                            # Start clockwise rotation sequence
                            rotation_sequence = "cw"
                            sequence_state = "forward"
                            sequence_start_time = current_time
                            direction_1, direction_2, direction_3 = 128 + 5, 128, 128  # Move forward
                            state = "cw_sequence_forward"
                            print("Initiating clockwise rotation sequence: Moving forward.")
                        elif direction == "ccw":
                            # Start counterclockwise rotation sequence
                            rotation_sequence = "ccw"
                            sequence_state = "forward"
                            sequence_start_time = current_time
                            direction_1, direction_2, direction_3 = 128 + 5, 128, 128  # Move forward
                            state = "ccw_sequence_forward"
                            print("Initiating counterclockwise rotation sequence: Moving forward.")
                        else:
                            direction_1, direction_2, direction_3 = 128, 128, 128  # Unknown, stop
                            state = "stopped"

                        # Display angle and direction on the output frame
                        if y2 != y1:
                            t = (center_y - y1) / (y2 - y1)
                            intersect_x = int(x1 + t * (x2 - x1))
                            intersect_y = center_y
                            cv2.circle(output, (intersect_x, intersect_y), 5, (0, 0, 255), -1)
                            cv2.putText(output, f"{angle_deg:.2f} deg", (intersect_x + 10, intersect_y - 10), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                            cv2.putText(output, direction, (intersect_x + 10, intersect_y + 20), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                        detected = True  # Line detected and processed
                        break  # Process only the first relevant line

                if not detected:
                    # No line crossing the center was detected
                    print("No yellow line crossing the center detected.")
                    direction_1, direction_2, direction_3 = 128, 128, 128  # Stop
                    state = "stopped"
            else:
                # No lines detected
                print("No yellow line detected.")
                direction_1, direction_2, direction_3 = 128, 128, 128  # Stop
                state = "stopped"

        # Display the output frame
        cv2.imshow('Yellow Line Detection Live', output)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

def main():
    global direction_1, direction_2, direction_3, state

    try:
        # Initialize serial port (adjust the port name as needed)
        port = serial.Serial(port="/dev/ttyAMA2", baudrate=115200, timeout=0.1)
        time.sleep(2)  # Wait for the serial port to initialize

        # Initialize directions to stop
        direction_1, direction_2, direction_3 = 128, 128, 128
        state = "stopped"

        # Start the move_robot thread
        move_thread = threading.Thread(target=move_robot, args=(port,), daemon=True)
        move_thread.start()

        # Start lane detection and command update
        calculate_yellow_line_angle_live()

    except serial.SerialException as e:
        print(f"Failed to open serial port: {e}")

    finally:
        # On exit, send stop command
        send_wheel_command(port, 128, 128, 128)
        time.sleep(0.1)  # Ensure the stop command is sent

        # Close the serial port
        if 'port' in locals() and port.is_open:
            port.close()
        print("Serial port closed. Program terminated.")

if __name__ == "__main__":
    main()
