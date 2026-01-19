import launch
import launch_ros

def generate_launch_description():
    """
    产生launch描述
    """
    # action_node_learn_face_detect = launch_ros.actions.Node(
    #     package='demo_python_service',   #功能包的名字
    #     executable='learn_face_detect',   #可执行文件的名字
    #     output='screen'  #日志输出的目的地,可选有screen/log/both
    # )
    
    action_node_face_detect_node = launch_ros.actions.Node(
        package='demo_python_service',   #功能包的名字
        executable='face_detect_node',   #可执行文件的名字
        output='screen'  #日志输出的目的地,可选有screen/log/both
    )
     
    action_node_face_detect_client_node = launch_ros.actions.Node(
        package='demo_python_service',   #功能包的名字
        executable='face_detect_client_node',   #可执行文件的名字
        output='screen'  #日志输出的目的地,可选有screen/log/both
    )
    return launch.LaunchDescription([
        # actions动作
        action_node_face_detect_node,
        action_node_face_detect_client_node,
    ])
    