#include <geometry_msgs/msg/transform_stamped.hpp> //提供消息接口
#include "rclcpp/rclcpp.hpp"
#include "tf2/LinearMath/Quaternion.h"             //提供tf2::Quaternion类
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp> //消息类型转换函数
#include <tf2_ros/transform_listener.h>            //坐标监听类，使用这个类可以监听查询到/tf,/tf_static话题的所有数据
#include <chrono>
#include <tf2_ros/buffer.h> //提供Buffer
#include <tf2/utils.h>      //提供了四元数转换为欧拉角的方法

using namespace std::chrono_literals; // 可以使用s,ms表示时间
class TFListener : public rclcpp::Node
{
private:
    std::shared_ptr<tf2_ros::TransformListener> listener_;
    rclcpp::TimerBase::SharedPtr timer_;
    std::shared_ptr<tf2_ros::Buffer> buffer_;

public:
    TFListener() : Node("tf_listener")
    {
        this->buffer_ = std::make_shared<tf2_ros::Buffer>(this->get_clock());
        this->listener_ = std::make_shared<tf2_ros::TransformListener>(*buffer_, this);
        timer_ = this->create_wall_timer(1s, std::bind(&TFListener::get_transform, this)); // 将成员函数当做回调函数
    };

    void get_transform()
    {
        // 到Buffer中查询坐标关系
        try
        {
            // 查询坐标关系
            const auto transform = buffer_->lookupTransform(
                "base_link",
                "target_point",
                this->get_clock()->now(),
                rclcpp::Duration::from_seconds(1.0f)); // this->get_clock()->now()表示查询最新的坐标信息，rclcpp::Duration::from_seconds(1)表示超时时间，超过1s未查询到就抛出异常
            // 获取查询结果
            auto translation = transform.transform.translation;
            auto rotation = transform.transform.rotation;
            // 四元数转换成欧拉角
            double y,p,r;
            tf2::getEulerYPR(rotation, y,p,r);
            RCLCPP_INFO(get_logger(), "平移%f,%f,%f", translation.x, translation.y, translation.z);
            RCLCPP_INFO(get_logger(), "旋转%f,%f,%f", y, p, r);

        }
        catch (const std::exception &e)
        {
            RCLCPP_WARN(this->get_logger(), "%s", e.what());
        };
    }
    // void publish_tf()
    // {
    //     //定义消息接口
    //     geometry_msgs::msg::TransformStamped transform;
    //     transform.header.stamp = this->get_clock()->now();
    //     transform.header.frame_id = "map";
    //     transform.child_frame_id = "base_link";
    //     transform.transform.translation.x = 2.0;
    //     transform.transform.translation.y = 3.0;
    //     transform.transform.translation.z = 0.0;
    //     tf2::Quaternion q;
    //     q.setRPY(0.0, 0.0, 30*M_PI/180);  //将弧度制欧拉角度值转换为四元数
    //     transform.transform.rotation = tf2::toMsg(q);   //将四元数对象转换成需要的对象
    //     //发布静态坐标关系
    //     this->listener_->sendTransform(transform);
    // }
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TFListener>();
    rclcpp::spin(node);
    rclcpp::shutdown();
}