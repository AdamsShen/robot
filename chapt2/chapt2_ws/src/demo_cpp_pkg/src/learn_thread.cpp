#include <iostream>
#include <thread> //多线程相关
#include <chrono> //时间相关
#include <functional>
#include <cpp-httplib/httplib.h> //下载相关

class Download
{
private:
    /* data */
public:
    void download(const std::string &host, const std::string &path,
                  const std::function<void(const std::string &, const std::string &)> &callback_world_count)
    {
        std::cout << "线程" << std::this_thread::get_id() << std::endl;
        httplib::Client client(host);
        auto response = client.Get(path);
        if (response && response->status == 200)
        {
            callback_world_count(path, response->body);
        }else {
            std::cout<<"错误"<<std::endl;
        }
    };
    void start_download(const std::string &host, const std::string &path,
                        const std::function<void(const std::string &, const std::string &)> &callback_world_count)
    {
        std::thread thread(std::bind(&Download::download, this, std::placeholders::_1, std::placeholders::_2, std::placeholders::_3),
                           host, path, callback_world_count);
        thread.detach();
    };
};

int main()
{
    auto d = Download();
    auto world_count = [](const std::string &path, const std::string &result) -> void
    {
        std::cout << "下载完成" << path << ":" << result.length() << ":" << result.substr(0, 9) << std::endl;
    };

    d.start_download("http://baidu.com", "/1.txt", world_count);
    d.start_download("http://baidu.com", "/2.txt", world_count);
    d.start_download("http://baidu.com", "/3.txt", world_count);

    // 主线程休眠10s
    std::this_thread::sleep_for(std::chrono::milliseconds(1000 * 10));

    return 0;
}
