cmake_minimum_required(VERSION 3.8)
project(status_display)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(status_interfaces REQUIRED)
find_package(Qt5 REQUIRED COMPONENTS Widgets)

add_executable(hello_qt src/hello_qt.cpp)
#qt5 不是来自于ros2 ament_target_dependencies依赖库方式是ros2提供的快速依赖工具，所以需要使用原生C++方式去依赖
target_link_libraries(hello_qt Qt5::Widgets)

add_executable(sys_status_display src/sys_status_display.cpp)
#链接qt5库
target_link_libraries(sys_status_display Qt5::Widgets)
#链接ros2相关的库
ament_target_dependencies(sys_status_display rclcpp status_interfaces)


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

install(TARGETS 
  hello_qt sys_status_display
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
