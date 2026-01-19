import launch
import launch_ros

def generate_launch_description():
    #1.声明一个launch参数
    action_declare_arg_background_g = launch.actions.DeclareLaunchArgument('launch_arg_bg', default_value='150')
    
    #2.将launch的参数手动传递给某一个节点
    
    """
    产生launch描述
    """
    action_node_turtlesim_node = launch_ros.actions.Node(
        package='turtlesim',   #功能包的名字
        executable='turtlesim_node',   #可执行文件的名字
        output='screen',  #日志输出的目的地,可选有screen/log/both
        parameters=[{'background_g': launch.substitutions.LaunchConfiguration('launch_arg_bg', default='150')}]   #LaunchConfiguration将launch中的launch_arg_bg参数取出并设置在的background_g值中
    )
     
    action_node_turtle_control = launch_ros.actions.Node(
        package='demo_cpp_service',   #功能包的名字
        executable='turtle_control',   #可执行文件的名字
        output='screen'  #日志输出的目的地,可选有screen/log/both
    )
    
    action_node_partol_client = launch_ros.actions.Node(
        package='demo_cpp_service',   #功能包的名字
        executable='partol_client',   #可执行文件的名字
        output='screen'  #日志输出的目的地,可选有screen/log/both
    )
    return launch.LaunchDescription([
        # actions动作
        action_declare_arg_background_g,
        action_node_turtlesim_node,
        action_node_turtle_control,
        action_node_partol_client,
    ])
    