#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <turtlesim/msg/pose.hpp>
#include <chrono>

using namespace std::chrono_literals;

class TurtlrControlNode : public rclcpp::Node
{
private:
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_; // 发布者的智能共享指针
    // rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr subscriber_; // 订阅者的智能共享指针
    double target_x_{1.0};
    double target_y_{1.0};
    double k_{1.0};         // 比例系数
    double max_speed_{3.0}; // 最大速度

public:
    explicit TurtlrControlNode(const std::string &node_name) : Node(node_name)
    {
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
        // timer_ = this->create_wall_timer(1000ms, std::bind(&TurtlrControlNode::time_callback, this));
        subscriber_ = this->create_subscription<turtlesim::msg::Pose>("/turtle1/pose", 10,
                                                                      std::bind(&TurtlrControlNode::on_pose_received, this, std::placeholders::_1));
    }

    void on_pose_received(const turtlesim::msg::Pose::SharedPtr pose) // 参数，收到数据的共享指针
    {
        // 1. 获取到当前的位置
        auto current_x = pose->x;
        auto current_y = pose->y;
        RCLCPP_INFO(get_logger(), "当前:x=%f,y=%f", current_x, current_y);

        // 2. 计算当前位置和目标位置的距离
        auto distance = std::sqrt(
            (target_x_ - current_x) * (target_x_ - current_x) +
            (target_y_ - current_y) * (target_y_ - current_y));

        // 3. 计算当前朝向和目标点相对当前位置朝向的角度差
        auto angle = std::atan2(target_y_ - current_y, target_x_ - current_x) - pose->theta;

        // 4. 计算线速度和角速度,控制策略
        auto msg = geometry_msgs::msg::Twist();
        if (distance > 0.1)
        {
            if (fabs(angle) > 0.2)
            {
                msg.angular.z = fabs(angle);
            }
            else
            {
                msg.linear.x = k_ * distance;
            }
        }

        //5. 限制线速度最大值
        if(msg.linear.x > max_speed_)
        {
            msg.linear.x = max_speed_;
        }

        // 发布消息
        this->publisher_->publish(msg);
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto circle_node = std::make_shared<TurtlrControlNode>("turtle_control_node");
    rclcpp::spin(circle_node);
    rclcpp::shutdown();

    return 0;
}