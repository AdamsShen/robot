import rclpy

from rclpy.node import Node

from demo_python_pkg.person_node import PersonNode

class WriterNode(Node):
    def __init__(self, node_name:str, book:str) -> None:
        print('WriterNode __init__ 方法被调用了')
        # super().__init__(name, age)  # 调用父类的方法
        super().__init__(node_name)
        self.book = book

def main():
    rclpy.init()
    node = WriterNode('zhangsan', '论快速入狱')
    # node.eat('yuxiangrousi')
    
    node.get_logger().info('2324324')
    rclpy.spin(node)
    rclpy.shutdown()