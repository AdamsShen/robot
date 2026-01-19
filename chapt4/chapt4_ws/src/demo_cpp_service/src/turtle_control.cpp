#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <turtlesim/msg/pose.hpp>
#include <chrono>
#include <chapt4_interfaces/srv/partol.hpp>
#include <rcl_interfaces/msg/set_parameters_result.hpp>

using Partol = chapt4_interfaces::srv::Partol;
using SetParametersResult = rcl_interfaces::msg::SetParametersResult;

class TurtlrControlNode : public rclcpp::Node
{
private:
    OnSetParametersCallbackHandle::SharedPtr parameter_callback_handler_;
    rclcpp::Service<Partol>::SharedPtr partol_service;
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
        //声明参数和获取参数的初始值
        this->declare_parameter("k", 1.0);
        this->declare_parameter("max_speed", 1.0);
        this->get_parameter("k", k_);
        this->get_parameter("max_speed", max_speed_);
        // 设置ros2自身节点参数的方法
        // this->set_parameter(rclcpp::Parameter("k", 2.0));
        
        //监听ros2参数更新函数回调，在ros2参数更新时第一时间更新成员变量中的值
        parameter_callback_handler_ = this->add_on_set_parameters_callback([&](const std::vector<rclcpp::Parameter> & parameters) -> SetParametersResult {
            SetParametersResult result;
            result.successful = true;
            for (const auto & parameter: parameters) {
                RCLCPP_INFO(this->get_logger(), "更新后的参数值为%s=%f", parameter.get_name().c_str(), parameter.as_double());
                if(parameter.get_name() == "k") {
                    this->k_ = parameter.as_double();
                }else if(parameter.get_name() == "max_speed") {
                    this->max_speed_ = parameter.as_double();
                }
            }
            return result;
        });
        partol_service = this->create_service<Partol>("partol", [&](const Partol::Request::SharedPtr requset, Partol::Response::SharedPtr response) -> void
                                                      {
            if((requset->target_x > 0 && requset->target_x < 12.0f) &&
                (requset->target_y > 0 && requset->target_y < 12.0f)) 
            {
                this->target_x_ = requset->target_x;
                this->target_y_ = requset->target_y;
                response->result = Partol::Response::SUCCESS;
            }else {
                response->result = Partol::Response::FAIL;
            }
            //由于在c++中response使用的是指针引用，所以不需要返回response，调用方就可以拿到response的结果
        });
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

        // 5. 限制线速度最大值
        if (msg.linear.x > max_speed_)
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