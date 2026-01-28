import launch
import launch_ros
from ament_index_python.packages import (
    get_package_share_directory,
)  # 用于定位urdf文件找到，然后让robot-state-publisher进行加载
import os


def generate_launch_description():
    # 获取功能包的share路径
    urdf_package_path = get_package_share_directory("fishbot_description")
    default_xacro_path = os.path.join(urdf_package_path, "urdf", "fishbot/fishbot.urdf.xacro")
    #获取rviz文件的路径,这个路径可以传入到rviz2节点启动命令中，这样rviz2命令在打开时就是一个已有数据的界面
    # default_rviz_path = os.path.join(urdf_package_path, "config", "display_robt_model.rviz")
    
    # 获取默认的gazebo的world文件路径
    default_gazebo_world_path = os.path.join(urdf_package_path, "world", "custom_room.world")
    # 声明一个xacro目录的参数，方便进行修改
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name="model",
        default_value=str(default_xacro_path),
        description="加载的模型文件路径"
    )
    # 通过urdf的文件路径获取内容，并转换成参数值对象，以供传入 robot_state_publisher节点中
    # substitutions_command_result = launch.substitutions.Command(['cat ', launch.substitutions.LaunchConfiguration('model')])   #使用cmd命令获取到了文件内容，'cat 文件'，这是一个命令，应该用数组传入，'cat ' 这个地方需要一个空格，不然会报错
    
    #对应xacro文件，可以使用'xacro xxx.xacro'命令将xacro文件转换成urdf文件并返回内容
    substitutions_command_result = launch.substitutions.Command(['xacro ', launch.substitutions.LaunchConfiguration('model')])   #使用xacro命令获取到了文件内容，'xacro 文件'，这是一个命令，应该用数组传入，'xacro ' 这个地方需要一个空格，不然会报错
    
    #转换成参数值对象
    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(substitutions_command_result, value_type=str)
    

    # 启动robot_state_publisher节点的命令
    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',   #功能包的名字
        executable='robot_state_publisher',   #可执行文件的名字
        #parameters是将参数值传递给节点的参数,这个相当于是ros2 run 功能包 可执行文件 --ros-args -p robot_description={robot_description_value}
        parameters=[{'robot_description': robot_description_value}]    # 功能包可以输入的参数配置
        
    )
    
    #启动gazebo，并加载指定的world，默认是custom_room.world文件
    action_launch_gazebo = launch.actions.IncludeLaunchDescription(
         launch.launch_description_sources.PythonLaunchDescriptionSource(
            [get_package_share_directory('gazebo_ros'), '/launch/', 'gazebo.launch.py']
        ),
         #('verbose', 'true')这个表示日志级别，true：表示详细输出日志；('world', default_gazebo_world_path)表示参数world的值是default_gazebo_world_path
         launch_arguments=[('world', default_gazebo_world_path), ('verbose', 'true')]  
    )
    
    #将您在 URDF/Xacro 文件中定义的机器人模型实例化到 Gazebo 的仿真世界中
    action_spawn_entity = launch_ros.actions.Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        #arguments就是在节点命令行中添加后续命令,此时相当于运行ros2 run gazebo_ros spawn_entity.py -topic /robot_description -entity fishbot
        arguments=['-topic', '/robot_description', '-entity', 'fishbot']
    )
    
    # 启动joint_state_publisher节点的命令，用来模拟机器人的关节角度
    # action_joint_state_publisher = launch_ros.actions.Node(
    #     package='joint_state_publisher',   #功能包的名字
    #     executable='joint_state_publisher',   #可执行文件的名字
    # )
    
    # 启动rviz2节点的命令
    # action_rviz_node = launch_ros.actions.Node(
    #     package='rviz2',   #功能包的名字
    #     executable='rviz2',   #可执行文件的名字
    #     #arguments就是在节点命令行中添加后续命令,此时相当于运行ros2 run rviz2 rviz2 -d {default_rviz_path}
    #     arguments=['-d', default_rviz_path]  
    # )
    
    #加载并激活fishbot_joint_state_broadcaster 关节状态控制器
    action_load_joint_state_controller = launch.actions.ExecuteProcess(
        cmd = 'ros2 control load_controller fishbot_joint_state_broadcaster --set-state active'.split(' '),
        output='screen'
    )
    
    #加载并激活fishbot_effort_controller 力控制器
    action_load_effort_controller = launch.actions.ExecuteProcess(
        cmd = 'ros2 control load_controller fishbot_effort_controller --set-state active'.split(' '),
        output='screen'
    )
    
    #加载并激活fishbot_diff_drive_controller 两轮差速控制器
    action_load_diff_drive_controller = launch.actions.ExecuteProcess(
        cmd = 'ros2 control load_controller fishbot_diff_drive_controller --set-state active'.split(' '),
        output='screen'
    )
    
    return launch.LaunchDescription([
        # actions动作
        action_declare_arg_mode_path,
        action_robot_state_publisher,
        action_launch_gazebo,
        action_spawn_entity,
        #下面这个是注册一个动作监听事件，等到action_spawn_entity这个动作执行完退出之后再执行action_load_joint_state_controller动作
        launch.actions.RegisterEventHandler( 
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=action_spawn_entity,
                on_exit=[action_load_joint_state_controller]
            )
        ),
        #下面这个是注册一个动作监听事件，等到action_load_joint_state_controller这个动作执行完退出之后再执行action_load_effort_controller动作
        launch.actions.RegisterEventHandler( 
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=action_load_joint_state_controller,
                on_exit=[action_load_diff_drive_controller]   #力控制器和两轮差速控制器都是控制机器人轮子的，只能同时执行一个动作
            )
        ),
    ])
