#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <turtlesim/msg/pose.hpp>
#include <chrono>

using namespace std::chrono_literals;

class TurtlrControlNode : public rclcpp::Node
{
private:
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;   // 发布者的智能共享指针
    rclcpp::TimerBase::SharedPtr timer_;    //定时器的智能共享指针
public:
    explicit TurtlrControlNode(const std::string &node_name) : Node(node_name)
    {
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
        timer_ = this->create_wall_timer(1000ms, std::bind(&TurtlrControlNode::time_callback, this));

        // timer_ = this->create_wall_timer(1000ms, [&]() -> void {
        //     auto msg = geometry_msgs::msg::Twist();
        //     msg.linear.x = 1.0;
        //     msg.angular.z = 0.5;
        //     // 发布消息
        //     this->publisher_->publish(msg);
        // });
    }

    void time_callback()
    {
        auto msg = geometry_msgs::msg::Twist();
        msg.linear.x = 1.0;
        // msg.linear.y = 1.0;
        msg.angular.z = 0.5;
        // 发布消息
        this->publisher_->publish(msg);
    }
};

int main(int argc, char **argv) 
{
    rclcpp::init(argc, argv);
    auto circle_node = std::make_shared<TurtlrControlNode>("turtle_circle_node");
    rclcpp::spin(circle_node);
    rclcpp::shutdown();

    return 0;
}