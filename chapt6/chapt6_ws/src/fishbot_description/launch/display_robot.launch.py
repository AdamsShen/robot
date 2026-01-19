import launch
import launch_ros
from ament_index_python.packages import (
    get_package_share_directory,
)  # 用于定位urdf文件找到，然后让robot-state-publisher进行加载
import os


def generate_launch_description():
    # 获取默认的urdf路径
    urdf_package_path = get_package_share_directory("fishbot_description")
    default_urdf_path = os.path.join(urdf_package_path, "urdf", "first_robot.urdf")
    #获取rviz文件的路径,这个路径可以传入到rviz2节点启动命令中，这样rviz2命令在打开时就是一个已有数据的界面
    default_rviz_path = os.path.join(urdf_package_path, "config", "display_robt_model.rviz")
    # 声明一个urdf目录的参数，方便进行修改
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name="model",
        default_value=str(default_urdf_path),
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
    
    # 启动joint_state_publisher节点的命令
    action_joint_state_publisher = launch_ros.actions.Node(
        package='joint_state_publisher',   #功能包的名字
        executable='joint_state_publisher',   #可执行文件的名字
        
    )
    
    # 启动rviz2节点的命令
    action_rviz_node = launch_ros.actions.Node(
        package='rviz2',   #功能包的名字
        executable='rviz2',   #可执行文件的名字
        #arguments就是在节点命令行中添加后续命令,此时相当于运行ros2 run rviz2 rviz2 -d {default_rviz_path}
        arguments=['-d', default_rviz_path]  
    )
    
    return launch.LaunchDescription([
        # actions动作
        action_declare_arg_mode_path,
        action_robot_state_publisher,
        action_joint_state_publisher,
        action_rviz_node
    ])
