from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    package_dir = FindPackageShare('depth_camera_gazebo')
    pkg_gazebo_ros = FindPackageShare('gazebo_ros')
    rviz_config_dir = PathJoinSubstitution([package_dir, 'rviz', 'urdf.rviz'])
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_dir],
        parameters=[{'use_sim_time': True}]
        )

    xacro_path = PathJoinSubstitution([package_dir, 'urdf', 'gazebo_d435_camera.urdf.xacro'])
    robot_description_content = ParameterValue(
                                    Command(['xacro ', xacro_path,
                                             ' use_nominal_extrinsics:=true',
                                             ' publish_pointcloud:=true'
                                            ]), value_type=str)
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description_content,
            'publish_frequency': 30.0,
            'use_sim_time': True
        }]
    )

    # Launch Gazebo
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([pkg_gazebo_ros, 'launch', 'gazebo.launch.py'])
        )
    )

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=[ '-entity', 'realsense_d435',
                                    '-topic', 'robot_description',
                                    '-z', '0.5'
                                  ],
                        output='screen')

    return LaunchDescription([
        rviz_node,
        robot_state_publisher_node,
        gazebo_launch,
        spawn_entity
    ])
