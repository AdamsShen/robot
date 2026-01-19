import rclpy 
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector
import face_recognition
import cv2  #opencv
from ament_index_python.packages import get_package_share_directory  #用于获取功能包share目录，绝对路径
import os
from cv_bridge import CvBridge #一个类
import time
from rcl_interfaces.msg import SetParametersResult

class FaceDetectNode(Node):
    def __init__(self):
        super().__init__('face_detect_node')
        #第一个参数是服务类型相当于接口名称，第二个参数是服务名,第三个参数就是接口的实现过程或者说是接口实现回调
        #下面这个FaceDetector接口中定义的就相当于接口参数和接口返回值
        """
        sensor_msgs/Image image   #人脸图像，接口参数
        ---  以下是接口返回值
        int16 number #人脸数量 
        float32 use_time #识别耗时
        int32[] top  # 人脸位置
        int32[] right
        int32[] bottom
        int32[] left
        """
        self.service_ = self.create_service(FaceDetector, 'face_detect', self.detect_face_callback)
        self.bridge = CvBridge()
        # 参数声明设置,将代码中的参数ros2化，可以在启动ros2时指定参数
        self.declare_parameter('number_of_times_to_upsample', 1)
        self.declare_parameter('model', 'hog')
        self.number_of_times_to_upsample = self.get_parameter('number_of_times_to_upsample').value
        self.model = self.get_parameter('model').value
        self.add_on_set_parameters_callback(self.parameters_callback)
        # 设置ros2自身节点参数的方法
        # self.set_parameters([rclpy.Parameter('model', rclpy.Parameter.Type.STRING, 'cnn')])
        
        # self.number_of_times_to_upsample = 1
        # self.model = 'hog'
        self.default_image_path = os.path.join(get_package_share_directory("demo_python_service"), "resource/default.jpg")
        self.get_logger().info(f'人脸检测服务已经启动')
        
    def parameters_callback(self, paramters):
        for paramter in paramters:
            self.get_logger().info(f"参数名：{paramter.name}, 参数值：{paramter.value}")
            if paramter.name == 'number_of_times_to_upsample':
                self.number_of_times_to_upsample = paramter.value
            if paramter.name == 'model':
                self.model = paramter.value
        
        return SetParametersResult(successful=True)

    def detect_face_callback(self, request, response):
        if request.image.data:
            cv_image = self.bridge.imgmsg_to_cv2(request.image)  #使用CvBridge将ros2中的image数据转换为cv可以识别的image数据
        else:
            # 使用opencv来加载图片
            cv_image = cv2.imread(self.default_image_path)
            self.get_logger().info(f'传入图像为空，使用默认图像!')
        #cv_image 已经是一个opencv格式的图像了
        start_time = time.time()
        self.get_logger().info(f'加载完成图像，开始识别!')
        # 检测人脸,返回人脸的位置，上下左右值
        face_locations = face_recognition.face_locations(cv_image, self.number_of_times_to_upsample, self.model)
        response.use_time = time.time() - start_time
        response.number = len(face_locations)  #face_locations是一个数组，它的长度就表示人脸的数量
        for top, right, bottom, left in face_locations:
            response.top.append(top)
            response.right.append(right)
            response.bottom.append(bottom)
            response.left.append(left)
        self.get_logger().info(f'识别完成！ 耗时:{response.use_time}')  
        return response   #python没有指针，必须返回response
    
     #获取图片的真实路径 /home/adams/chapt4/chapt4_ws/install/demo_python_service/share/demo_python_service
    # default_image_path = os.path.join(get_package_share_directory("demo_python_service"), "/resource/default.jpg")  #os.path.join函数会自动判断是否需要加入'/'
    # print(f"图片的真实路径:{default_image_path}")
    # # 使用opencv来加载图片
    # image = cv2.imread(default_image_path)
    # # 检测人脸,返回人脸的位置，上下左右值
    # face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=1, model='hog')
    # # 绘制人脸框
    # for top, rigth, bottom, left in face_locations:
        

def main():
    rclpy.init()
    node = FaceDetectNode()
    rclpy.spin(node)
    rclpy.shutdown()

