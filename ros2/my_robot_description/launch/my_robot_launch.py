from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    urdf_file = os.path.join(get_package_share_directory('my_robot_description'), 'urdf', 'my_robot.urdf')
    
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        # joint_state_publisher 노드
        Node(
            package='lidar_3d_package',
            executable='servo_tf_broadcaster',
            name='servo_tf_broadcaster',
            output='screen'
        ),

        # robot_state_publisher 노드
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_desc}]
        ),

        # RViz2 실행
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', os.path.join(get_package_share_directory('my_robot_description'), 'rviz', 'my_robot.rviz')]
        )
    ])
