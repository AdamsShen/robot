cmake_minimum_required(VERSION 3.8)
project(fishbot_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

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

#安装，将launch以及urdf目录以及所有文件拷贝到install目录下
install(DIRECTORY launch urdf config world  #launch urdf表示将launch以及urdf目录以及目录下所有文件都拷贝到install目录下,将config目录也拷贝到install目录下
  DESTINATION share/${PROJECT_NAME}  #这个表示目的地路径，最终会将launch以及urdf目录以及目录所有文件拷贝到share/${PROJECT_NAME}目录下
)

ament_package()
