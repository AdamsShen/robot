import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster  #动态坐标发布器
from geometry_msgs.msg import TransformStamped  #消息接口
from tf_transformations import quaternion_from_euler  #欧拉角转四元数函数
import math  #使用角度转弧度函数

class TFBroadcaster(Node):
    def __init__(self):
        super().__init__('tf_broadcaster')  #ros2节点名称
        self.tf_broadcaster = TransformBroadcaster(self)
        self.timer_ = self.create_timer(0.01, self.publisher_tf)  #创建定时器，0.01s发布一次动态坐标
        
    def publisher_tf(self):
        """
        发布TF，从camera_link --> bottle_link之间的坐标关系
        """
        transform = TransformStamped()
        transform.header.frame_id = 'camera_link'
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.child_frame_id = 'bottle_link'
        
        #平移部分进行赋值
        transform.transform.translation.x = 0.2
        transform.transform.translation.y = 0.3
        transform.transform.translation.z = 0.5
        # 欧拉角转四元数q=x,y,z,w
        q = quaternion_from_euler(0, 0, 0)  #用来将欧拉角转为四元数
        # 旋转部分进行赋值
        transform.transform.rotation.x = q[0]
        transform.transform.rotation.y = q[1]
        transform.transform.rotation.z = q[2]
        transform.transform.rotation.w = q[3]
        #坐标关系发布出去
        self.tf_broadcaster.sendTransform(transform)
        self.get_logger().info(f'发布TF:{transform}')

def main():
    rclpy.init()
    node = TFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()
    pass
        