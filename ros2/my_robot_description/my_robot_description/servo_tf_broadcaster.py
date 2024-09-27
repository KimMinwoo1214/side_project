import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import math
import serial

class LidarRotator(Node):
    def __init__(self):
        super().__init__('lidar_rotator')
        self.broadcaster = TransformBroadcaster(self)

        # Timer for broadcasting transforms
        self.timer = self.create_timer(0.015, self.broadcast_transform)

        # Open serial port to Arduino for rotation angles
        self.serial_port = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)
        self.angle = -60.0  # Default angle in degrees

    def get_angle_from_arduino(self):
        try:
            # Read from serial port
            if self.serial_port.in_waiting > 0:
                arduino_data = self.serial_port.readline().decode('utf-8').strip()
                self.angle = float(arduino_data)
                self.get_logger().info(f"Received angle: {self.angle} degrees from Arduino")
        except Exception as e:
            self.get_logger().warn(f"Failed to read from serial: {e}")

    def broadcast_transform(self):
        # Get the latest angle from Arduino
        self.get_angle_from_arduino()

        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = "base_link"
        transform.child_frame_id = "lidar_frame"

        # Convert degrees to radians for the quaternion
        radians = math.radians(self.angle)
        transform.transform.rotation.x = math.sin(radians / 2.0)
        transform.transform.rotation.y = 0.0
        transform.transform.rotation.z = 0.0
        transform.transform.rotation.w = math.cos(radians / 2.0)

        # Broadcast the transform
        self.broadcaster.sendTransform(transform)

def main(args=None):
    rclpy.init(args=args)
    node = LidarRotator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
