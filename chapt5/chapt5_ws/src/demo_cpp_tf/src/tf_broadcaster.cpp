#include <geometry_msgs/msg/transform_stamped.hpp>  //提供消息接口
#include "rclcpp/rclcpp.hpp"
#include "tf2/LinearMath/Quaternion.h" //提供tf2::Quaternion类
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>  //消息类型转换函数
#include <tf2_ros/transform_broadcaster.h>  //坐标广播器类
#include <chrono>

using namespace std::chrono_literals;   // 可以使用s,ms表示时间
class TFBroadcaster: public rclcpp::Node
{
private:
    std::shared_ptr<tf2_ros::TransformBroadcaster> broadcaster_;
    rclcpp::TimerBase::SharedPtr timer_;
public:
    TFBroadcaster() :Node("tf_broadcaster")
    {
        broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);  //在里面创建一个发布者，用来发布/tf话题
        // this->publish_tf();
        timer_ = this->create_wall_timer(100ms, std::bind(& TFBroadcaster::publish_tf, this));      //将成员函数当做回调函数
    };

    void publish_tf()
    {
        //定义消息接口
        geometry_msgs::msg::TransformStamped transform;
        transform.header.stamp = this->get_clock()->now();
        transform.header.frame_id = "map";
        transform.child_frame_id = "base_link";
        transform.transform.translation.x = 2.0;
        transform.transform.translation.y = 3.0;
        transform.transform.translation.z = 0.0;
        tf2::Quaternion q;
        q.setRPY(0.0, 0.0, 30*M_PI/180);  //将弧度制欧拉角度值转换为四元数
        transform.transform.rotation = tf2::toMsg(q);   //将四元数对象转换成需要的对象
        //发布静态坐标关系
        this->broadcaster_->sendTransform(transform);
    }
};

int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TFBroadcaster>();
    rclcpp::spin(node);
    rclcpp::shutdown();
}