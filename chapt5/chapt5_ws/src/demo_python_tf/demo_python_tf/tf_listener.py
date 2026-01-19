import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer  # 坐标监听器，使用这个类可以监听查询到/tf,/tf_static话题的所有数据
from tf_transformations import (
    euler_from_quaternion,
)  # 四元数转欧拉角函数,坐标监听器监听到的数据是四元数形式数据
import math  # 使用角度转弧度函数


class TFBroadcaster(Node):
    def __init__(self):
        super().__init__("tf_listener")  # ros2节点名称
        self.buffer_ = Buffer()
        self.tf_listener = TransformListener(self.buffer_, self)
        self.timer_ = self.create_timer(
            1, self.get_transform
        )  # 创建定时器，1s获取一次坐标

    def get_transform(self):
        """
        实时查询，定时获取坐标关系
        """
        try:
            result = self.buffer_.lookup_transform(
                "base_link",
                "bottle_link",
                rclpy.time.Time(seconds=0.0),
                rclpy.time.Duration(seconds=1.0),
            )  # rclpy.time.Time(seconds=0)表示查询最新的坐标，rclpy.time.Time(seconds=1.0)表示超时时间1s查询不到就抛出异常
            transform = result.transform
            self.get_logger().info(f"监听到的数据为：{transform}")
            self.get_logger().info(f"监听到的数据平移：{transform.translation}")
            self.get_logger().info(f"监听到的数据旋转(四元数)：{transform.rotation}")
            transform_euler = euler_from_quaternion(
                [transform.rotation.x,
                transform.rotation.y,
                transform.rotation.z,
                transform.rotation.w]
            )
            self.get_logger().info(f"监听到的数据欧拉角(RPY)：{transform_euler}")

        except Exception as e:
            self.get_logger().warn(f'获取坐标变换失败，原因：{str(e)}')
            pass


def main():
    rclpy.init()
    node = TFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()
    pass
