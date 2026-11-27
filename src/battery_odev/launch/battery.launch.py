from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='battery_odev',
            executable='battery_node',
            name='battery_node',
            output='screen',
        ),
        Node(
            package='battery_odev',
            executable='monitor_node',
            name='monitor_node',
            output='screen',
        ),
    ])
