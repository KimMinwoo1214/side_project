import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from sensor_msgs.msg import JointState  # JointState 메시지
from std_msgs.msg import Header
import math
import serial

class LidarRotator(Node):
    def __init__(self):
        super().__init__('lidar_rotator')
        self.broadcaster = TransformBroadcaster(self)

        # Timer for broadcasting transforms and joint state
        self.timer = self.create_timer(0.015, self.update_lidar)

        # Publisher for JointState
        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)

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
        # Convert degrees to radians for the quaternion
        radians = math.radians(self.angle)

        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = "base_link"
        transform.child_frame_id = "lidar_frame"

        # Set translation (URDF에 따른 z = 0.018, x = 0, y = 0)
        # transform.transform.translation.x = 0.0
        # transform.transform.translation.y = 0.0
        # transform.transform.translation.z = 0.018

        # Set rotation (around the X-axis)
        transform.transform.rotation.x = math.sin(radians / 2.0)
        transform.transform.rotation.y = 0.0
        transform.transform.rotation.z = 0.0
        transform.transform.rotation.w = math.cos(radians / 2.0)

        # Broadcast the transform
        self.broadcaster.sendTransform(transform)


    def publish_joint_states(self):
        # JointState 메시지 생성
        joint_state = JointState()
        joint_state.header = Header()
        joint_state.header.stamp = self.get_clock().now().to_msg()

        # 조인트 이름은 URDF 파일과 동일해야 합니다.
        joint_state.name = ['base_to_lidar']

        # 현재 조인트 상태 (각도) 설정 (라디안 값으로 변환)
        joint_state.position = [math.radians(self.angle)]

        # JointState 퍼블리시
        self.joint_pub.publish(joint_state)

    def update_lidar(self):
        # Get the latest angle from Arduino
        self.get_angle_from_arduino()

        # Broadcast the transform (TF)
        self.broadcast_transform()

        # Publish joint state (JointState)
        self.publish_joint_states()

def main(args=None):
    rclpy.init(args=args)
    node = LidarRotator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
