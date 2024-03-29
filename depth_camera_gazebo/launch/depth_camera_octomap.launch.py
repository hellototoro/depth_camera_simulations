import os
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch.actions import ExecuteProcess

def generate_launch_description():
    package_dir = FindPackageShare('depth_camera_gazebo')
    depth_camera_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([package_dir, 'launch', 'depth_camera.launch.py'])
        )
    )

    octomap_server_node = Node(
            package='octomap_server',
            executable='octomap_server_node',
            name='octomap_server',
            parameters=[
                {'resolution': 0.01},
                {'frame_id': 'base_link'},
                {'sensor_model/max_range': 3.5},
                {'latch': False},
                {'sensor_model/hit': 0.7},
                {'sensor_model/miss': 0.4},
                {'sensor_model/min': 0.12},
                {'sensor_model/max': 0.97},
                {'pointcloud_max_z': 3.5},
                {'pointcloud_min_z': 0.12},
                {'occupancy_max_z': 3.5},
                {'occupancy_min_z': 0.12},
                {'filter_ground ': True},
            ],
            remappings=[
                ('/cloud_in', '/depth/color/points')
            ]
        )

    return LaunchDescription([
        depth_camera_node,
        octomap_server_node
    ])
