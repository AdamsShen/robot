import rclpy 
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector
import face_recognition
import cv2  #opencv
from ament_index_python.packages import get_package_share_directory  #用于获取功能包share目录，绝对路径
import os
from cv_bridge import CvBridge #一个类
import time
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter,ParameterValue,ParameterType


class FaceDetectClientNode(Node):
    def __init__(self):
        super().__init__('face_detect_client_node')
        self.bridge = CvBridge()
        self.default_image_path = os.path.join(get_package_share_directory("demo_python_service"), "resource/test1.jpg")
        self.get_logger().info(f'人脸检测客户端已经启动')
        self.client_ = self.create_client(FaceDetector, 'face_detect')
        self.image_ = cv2.imread(self.default_image_path)
        
    def call_set_parameters(self, parameters):
        """
        用于调用服务，修改参数值
        """
        #1. 创建客户端，等待服务上线
        update_param_client = self.create_client(SetParameters, '/face_detect_node/set_parameters')
        while update_param_client.wait_for_service(timeout_sec = 1.0) is False:
            self.get_logger().info('等待参数更新服务端上线！')
        #2. 构造request
        request = SetParameters.Request()
        request.parameters = parameters
        #3. 调用服务端更新参数的接口,并等待服务端处理完成
        future = update_param_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)  # 等待服务端返回响应
        response = future.result()    #获取响应结果
        return response
    
    def update_detect_model(self, model='hog'):
        """
        根据传入的model构造Parameters，然后调用call_set_parameters函数更新服务端的参数
        """
        #1. 创建参数对象
        param = Parameter()
        param.name = 'model'
        #2. 赋值
        # 创建param_value
        param_value = ParameterValue()
        param_value.string_value = model
        param_value.type = ParameterType.PARAMETER_STRING
        param.value = param_value
        #3.调用call_set_parameters，请求更新参数
        response = self.call_set_parameters([param])
        for result in response.results:
            if result.successful:
                self.get_logger().info(f"设置参数成功{result.successful}, 原因：{result.reason}")
            else :
                self.get_logger().warn(f"设置参数失败{result.successful}, 原因：{result.reason}")

    def send_request(self):
        # 1.判断服务端是否在线
        while self.client_.wait_for_service(timeout_sec = 1.0) is False:
            self.get_logger().info('等待服务端上线！')
        #2. 构造request
        request = FaceDetector.Request()
        request.image = self.bridge.cv2_to_imgmsg(self.image_)
        # 3. 发送请求到服务端，并等待服务端处理完成
        future = self.client_.call_async(request)    #异步发送请求，现在的future中并没有包含响应结果，需要等待服务端处理完成才会将结果放在future中
        # while not future.done():
        #     time.sleep(1.0)  #休眠当前线程，等待服务处理完成 === 造成当前线程无法再接受来自服务端的返回，导致永远没有办法完成future.done(),无法返回true
        rclpy.spin_until_future_complete(self, future)  #在后台去查看future是否完成，而不影响spin监听的使用，即不会阻塞主线程spin逻辑，服务端返回结果后会放在future中的result中
        #上面一行的另一种实现方式，通过回调函数的方式进行实现
        # def result_callback(result_future):
        #     response = result_future.result()  #获取响应结果
        #     self.get_logger().info(f"接收到响应，共有{response.number}张人脸, 耗时{response.use_time}s")
        #     self.show_response(response)
        #     pass
        # future.add_done_callback(result_callback)
        
        response = future.result()  #获取响应结果
        self.get_logger().info(f"接收到响应，共有{response.number}张人脸, 耗时{response.use_time}s")
        #self.show_response(response)
        
        
    
    def show_response(self, response):
        for i in range(response.number):
            top  = response.top[i]
            right  = response.right[i]
            bottom  = response.bottom[i]
            left  = response.left[i]
            # 绘制人脸框
            cv2.rectangle(self.image_, (left, top), (right, bottom), (255, 0, 0), 4)  # (255, 0, 0)表示红色，4表示矩形框的宽度
        # 结果显示
        cv2.imshow('Face Detecte Result', self.image_)
        # 等待按键，然后退出,这个也是阻塞的,会导致spin无法正常运行
        cv2.waitKey(0)
        
def main():
    rclpy.init()
    node = FaceDetectClientNode()
    #修改ros2参数model的值
    node.update_detect_model('hog')
    node.send_request()  #调用send_request, 里面不能阻塞，否则rclpy.spin无法进行监听node
     #再次修改ros2参数model的值
    node.update_detect_model('cnn')
    node.send_request()  #调用send_request, 里面不能阻塞，否则rclpy.spin无法进行监听node
    
    rclpy.spin(node)
    rclpy.shutdown()