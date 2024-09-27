from setuptools import setup

package_name = 'lidar_3d_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/servo_check.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hspark',
    maintainer_email='hspark@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
    'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'lidar_tf_broadcaster = lidar_3d_package.lidar_tf_broadcaster:main',
            'lidar_to_pointcloud = lidar_3d_package.lidar_to_pointcloud:main',
            'servo_tf_broadcaster = lidar_3d_package.servo_tf_broadcaster:main',
        ],
    },
)
