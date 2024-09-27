from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # 서보모터의 좌표 변환을 퍼블리시하는 노드
    servo_tf_broadcaster = Node(
        package='lidar_3d_package',  # 'servo_tf_broadcaster.py'가 있는 패키지 이름
        executable='servo_tf_broadcaster',  # 이 파일의 실행 파일 이름
        name='servo_tf_broadcaster',
        output='screen',
    )

    return LaunchDescription([
        servo_tf_broadcaster,
    ])
