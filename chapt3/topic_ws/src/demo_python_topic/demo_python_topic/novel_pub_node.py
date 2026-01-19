import rclpy
from rclpy.node import Node
import requests
from example_interfaces.msg import String
from queue import Queue

class NovelPubNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name}, 启动！')
        
        # 加入_下划线 表示成员变量
        self.novels_queue_ = Queue()  #创建队列
        self.novel_publisher_ = self.create_publisher(String, "novel", 10)  # 创建话题发布者
        self.create_timer(5, self.timer_callback)  #创建定时器
    
    def timer_callback(self):
        if self.novels_queue_.qsize() > 0:
            line = self.novels_queue_.get()
            msg = String()  #组装消息
            msg.data = line
            self.novel_publisher_.publish(msg)   #发布消息
            self.get_logger().info(f'发布了: {msg}')
        # pass
    
    def download(self, url):
        response = requests.get(url)
        response.encoding = "utf-8"
        self.get_logger().info(f'下载 {url}, 长度：{len(response.text)}, 内容：{response.text}')
        text = response.text
        for line in text.splitlines():
            self.novels_queue_.put(line)

def main():
    rclpy.init()
    node = NovelPubNode('novel_pub')
    node.download("http://172.23.137.70:8000//novel1.txt");
    rclpy.spin(node)
    rclpy.shutdown()