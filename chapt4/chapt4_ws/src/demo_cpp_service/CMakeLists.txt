cmake_minimum_required(VERSION 3.8)
project(demo_cpp_service)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(chapt4_interfaces REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(turtlesim REQUIRED)


#添加可执行文件
add_executable(turtle_control src/turtle_control.cpp)
add_executable(partol_client src/partol_client.cpp)
#链接依赖
ament_target_dependencies(turtle_control chapt4_interfaces rclcpp geometry_msgs turtlesim)
ament_target_dependencies(partol_client chapt4_interfaces rclcpp)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

#安装，将文件拷贝到install目录下
install(TARGETS
  turtle_control partol_client
  DESTINATION lib/${PROJECT_NAME}
)

#安装launch，将launch目录以及所有文件拷贝到install目录下
install(DIRECTORY launch   #launch表示将launch目录以及目录下所有文件都拷贝到install目录下
  DESTINATION share/${PROJECT_NAME} #这个表示目的地路径，最终会将launch目录以及目录所有文件拷贝到share/${PROJECT_NAME}目录下
)

ament_package()
