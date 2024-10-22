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

# Global variables for color range
color_range_1, color_range_2 = None, None  # Default to None (waiting for user input)
color_mode = None  # 'yellow' or 'blue'

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

def calculate_line_angle_live():
    """
    Capture video from the camera, detect yellow or blue lines, determine direction, and update wheel commands.
    """
    global direction_1, direction_2, direction_3, state
    global color_range_1, color_range_2, color_mode  # Access global color ranges

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

        # Define color range in HSV based on selected mode
        if color_mode == "yellow":
            lower_color = np.array([color_range_1, 100, 100])
            upper_color = np.array([color_range_2, 255, 255])
        elif color_mode == "blue":
            lower_color = np.array([100, 100, 100])
            upper_color = np.array([140, 255, 255])

        # Create color mask
        mask = cv2.inRange(hsv, lower_color, upper_color)

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
                    print(f"Direction: {'left' if angle_deg < 0 else 'right'}")

                    # Send direction to serial port
                    if angle_deg < 0:
                        direction_1, direction_2, direction_3 = 128, 128, 130  # Move left
                    else:
                        direction_1, direction_2, direction_3 = 128, 128, 126  # Move right
                    send_wheel_command(port, direction_1, direction_2, direction_3)

                    # Update wheel commands
                    detected = True  # Line detected and processed
                    break  # Process only the first relevant line

        if not detected:
            # No line crossing the center was detected
            print("No line crossing the center detected.")
            direction_1, direction_2, direction_3 = 128, 128, 128  # Stop

        # Display the output frame
        cv2.imshow('Line Detection Live', output)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

def main():
    global direction_1, direction_2, direction_3, state
    global color_range_1, color_range_2, color_mode  # Access global color ranges

    # Initialize serial port (adjust the port name as needed)
    port = serial.Serial(port="/dev/ttyAMA2", baudrate=115200, timeout=0.1)
    time.sleep(2)  # Wait for the serial port to initialize

    # Start with AGV stopped
    direction_1, direction_2, direction_3 = 128, 128, 128
    state = "stopped"

    try:
        while True:
            # Prompt user to select color to detect
            color_choice = input("Select color to detect (b for blue, y for yellow): ").strip().lower()

            if color_choice == "y":
                color_range_1, color_range_2 = 15, 35
                color_mode = "yellow"
                print("Color set to YELLOW. HSV ranges: lower =", color_range_1, "upper =", color_range_2)
            elif color_choice == "b":
                color_range_1, color_range_2 = 100, 140
                color_mode = "blue"
                print("Color set to BLUE. HSV ranges: lower =", color_range_1, "upper =", color_range_2)
            else:
                print("Invalid color choice. Please select either 'b' or 'y'.")

            # Start lane detection and command update
            calculate_line_angle_live()

    except serial.SerialException as e:
        print(f"Failed to open serial port: {e}")

    finally:
        try:
            # On exit, send stop command
            send_wheel_command(port, 128, 128, 128)
            time.sleep(0.1)  # Ensure the stop command is sent

            # Close the serial port
            if port.is_open:
                port.close()
            print("Serial port closed. Program terminated.")
        except Exception as e:
            print(f"Error closing serial port: {e}")

if __name__ == "__main__":
    main()
