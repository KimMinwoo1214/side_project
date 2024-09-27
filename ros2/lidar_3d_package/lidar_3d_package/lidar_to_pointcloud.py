import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, PointCloud2
from laser_geometry import LaserProjection
from tf2_ros import Buffer, TransformListener

class LidarToPointCloud(Node):
    def __init__(self):
        super().__init__('lidar_to_pointcloud')
        self.laser_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.pc_pub = self.create_publisher(PointCloud2, '/pointcloud', 10)
        self.lp = LaserProjection()
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

    def scan_callback(self, msg):
        try:
            # LiDAR 데이터를 base_frame으로 변환
            transform = self.tf_buffer.lookup_transform('base_frame', msg.header.frame_id, rclpy.time.Time())
            cloud = self.lp.projectLaser(msg, transform)
            self.pc_pub.publish(cloud)
        except Exception as e:
            self.get_logger().error(f'Error: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = LidarToPointCloud()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
