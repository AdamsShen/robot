#include <rclcpp/rclcpp.hpp>
#include <chapt4_interfaces/srv/partol.hpp>
#include <chrono>
#include <ctime>   //产生随机数
#include <rcl_interfaces/msg/parameter.hpp>
#include <rcl_interfaces/msg/parameter_type.hpp>
#include <rcl_interfaces/msg/parameter_value.hpp>
#include <rcl_interfaces/srv/set_parameters.hpp>

using namespace std::chrono_literals;  // 可以使用10s,100ms表示时间
using Partol = chapt4_interfaces::srv::Partol;
using SetP = rcl_interfaces::srv::SetParameters;

class PartolClient : public rclcpp::Node
{
private:
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Client<Partol>::SharedPtr partol_client_;
public:
    explicit PartolClient() : Node("partol_client")
    {
        partol_client_ = this->create_client<Partol>("partol");
        srand(time(NULL));   //初始化随机数种子
        timer_ = this->create_wall_timer(10s, [&]() -> void {
            //1.检测服务端是否上线
            while (!this->partol_client_->wait_for_service(1s))
            {
                if(!rclcpp::ok()){
                    RCLCPP_ERROR(this->get_logger(), "等待服务上线过程中，rclcpp挂了，我退下了");
                    return;
                };
                RCLCPP_INFO(this->get_logger(), "等待服务上线中....");
            }
            //2. 构造请求对象
            auto request = std::make_shared<Partol::Request>();
            request->target_x = rand() % 15;   //产生随机数，范围在0-14之间
            request->target_y = rand() % 15;   //产生随机数，范围在0-14之间

            RCLCPP_INFO(this->get_logger(), "准备好目标点%f, %f", request->target_x, request->target_y);
            //3. 使用partol_client_发送请求
            //异步调用，返回rclcpp::Client<Partol>::SharedFuture对象
            this->partol_client_->async_send_request(request, [&](rclcpp::Client<Partol>::SharedFuture result_future) -> void {
                auto response = result_future.get();
                if(response->result==Partol::Response::SUCCESS) {
                    RCLCPP_INFO(this->get_logger(), "请求巡逻目标点成功！");
                }else {
                    RCLCPP_INFO(this->get_logger(), "请求巡逻目标点失败！");
                }
            });
        });
    };

    /**
     * 创建客户端发送请求，返回结果
     */
    SetP::Response::SharedPtr callSetParameters(const rcl_interfaces::msg::Parameter & param)
    {
        auto param_client = this->create_client<SetP>("/turtle_control_node/set_parameters");
        //1.检测服务端是否上线
        while (!param_client->wait_for_service(1s))
        {
            if(!rclcpp::ok()){
                RCLCPP_ERROR(this->get_logger(), "等待服务上线过程中，rclcpp挂了，我退下了");
                return nullptr;   //返回一个空指针，不能返回空，因为函数返回值是指针
            };
            RCLCPP_INFO(this->get_logger(), "等待服务上线中....");
        }
        //2. 构造请求对象
        auto request = std::make_shared<SetP::Request>();
        request->parameters.push_back(param);

        //3. 使用param_client发送请求
        //异步调用，返回rclcpp::Client<Partol>::SharedFuture对象
        // param_client->async_send_request(request, [&](rclcpp::Client<Partol>::SharedFuture result_future) -> void {
        //     auto response = result_future.get();
        //     if(response->result==Partol::Response::SUCCESS) {
        //         RCLCPP_INFO(this->get_logger(), "请求巡逻目标点成功！");
        //     }else {
        //         RCLCPP_INFO(this->get_logger(), "请求巡逻目标点失败！");
        //     }
        // });

        //3. 使用param_client发送请求
        auto future = param_client->async_send_request(request);
        rclcpp::spin_until_future_complete(this->get_node_base_interface(), future);
        auto response = future.get();   //获取结果
        return response;
    };

    /**
     * 更新参数k
     */
    void update_server_param_k(double k) {
        //1. 创建参数对象
        auto param = rcl_interfaces::msg::Parameter();
        param.name = 'k';
        //2. 创建参数值
        auto param_value = rcl_interfaces::msg::ParameterValue();
        param_value.type = rcl_interfaces::msg::ParameterType::PARAMETER_DOUBLE;
        param_value.double_value = k;

        param.value = param_value;
        //3. 请求更新参数值，并处理
        auto response = this->callSetParameters(param);
        if(response == NULL) {
            RCLCPP_INFO(this->get_logger(), "参数更新失败！");
            return;
        }
        //遍历返回结果数组
        for(auto result:response->results) {
            if(result.successful == false) {
                RCLCPP_INFO(this->get_logger(), "参数更新失败！原因：%s", result.reason.c_str());
            }else {
                RCLCPP_INFO(this->get_logger(), "参数更新成功！");
            }
        }
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto partol_client_node = std::make_shared<PartolClient>();
    //调用更新参数k的方法
    partol_client_node->update_server_param_k(4.0);

    rclcpp::spin(partol_client_node);
    rclcpp::shutdown();

    return 0;
}