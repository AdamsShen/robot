import rclpy
from rclpy.node import Node

class PersonNode(Node): 
    def __init__(self,
                 node_name:str,
                 name: str,
                 age: int) -> None:
        print('PersonNode __init__ 方法被调用了，添加了两个属性')
        super().__init__(node_name)
        self.name = name
        self.age = age
    
    def eat(self, food_name: str):
        """
        eat 的 Docstring
        
        :param self: 说明
        :param food_name: 说明
        :type food_name: str
        """
        # print(f"{self.name}, {self.age}, 爱吃{food_name}")
        self.get_logger().info(f"{self.name}, {self.age}, 爱吃{food_name}")

def main():
    rclpy.init()
    node = PersonNode('zhangsan', '法外狂徒张三', 18)
    node1 = PersonNode('lisi', '法外狂徒李四', 89)
    node.eat('yuxiangrousi')
    node1.eat('西红柿')
    rclpy.spin(node)
    rclpy.spin(node1)
    rclpy.shutdown()