#include <QApplication>
#include <QLabel>
#include <QString>
#include <rclcpp/rclcpp.hpp>
#include <status_interfaces/msg/system_status.hpp>

using SystemStatus = status_interfaces::msg::SystemStatus;

class SysStatusDisplay : public rclcpp::Node
{
private:
    rclcpp::Subscription<SystemStatus>::SharedPtr subsciber_;
    QLabel *label;

public:
    SysStatusDisplay() : Node("sys_status_display")
    {
        label = new QLabel();
        subsciber_ = this->create_subscription<SystemStatus>("sys_status", 10, [&](const SystemStatus::SharedPtr msg) -> void
                                                             { label->setText(get_qstr_from_msg(msg)); });
        label->setText(get_qstr_from_msg(std::make_shared<SystemStatus>()));
        label->show();
    };

    QString get_qstr_from_msg(const SystemStatus::SharedPtr msg)
    {
        std::stringstream show_str;
        show_str << "====================新提供系统状态可视化工具===============================\n"
                 << "数据时间:\t" << msg->stamp.sec << "\ts\n"
                 << "主机名称:\t" << msg->host_name << "\t\n"
                 << "cpu使用率:\t" << msg->cpu_percent << "\t%\n"
                 << "内存使用率:\t" << msg->memory_percent << "\t%\n"
                 << "内存总大小:\t" << msg->memory_total << "\tMB\n"
                 << "内存可使用大小:\t" << msg->memory_available << "\tMB\n"
                 << "网络发送数据总量:\t" << msg->net_sent << "\tMB\n"
                 << "网络数据接收总量:\t" << msg->net_recv << "\tMB\n"
                 << "=============================================";
        return QString::fromStdString(show_str.str());
    };
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    QApplication app(argc, argv);
    auto node = std::make_shared<SysStatusDisplay>();
    std::thread spin_thread([&]() -> void
                            {
                                rclcpp::spin(node); // 阻塞代码,阻塞当前线程
                            });
    spin_thread.detach();   //分离线程，将新创建的线程与主线程分离
    app.exec(); // 执行应用，阻塞代码，直到退出，这里是退出qt界面

    return 0;
}