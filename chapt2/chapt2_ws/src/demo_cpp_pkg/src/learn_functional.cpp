#include <iostream>
#include <functional> //函数包装器头文件

// 自由函数
void save_with_free_fun(const std::string &file_name)
{
    std::cout << "自由函数" << file_name << std::endl;
}

class FileSave
{
private:
    /* data */
public:
    FileSave(/* args */) = default;
    ~FileSave() = default;

    // 成员函数
    void save_with_member_fun(const std::string &file_name)
    {
        std::cout << "成员方法" << file_name << std::endl;
    };
};

int main()
{
    FileSave file_save;
    // lambda函数
    auto save_with_lambda = [](const std::string &file_name) -> void
    {
        std::cout << "lambda函数" << file_name << std::endl;
    };

    // 调用方式
    //  save_with_free_fun("file.txt");
    //  file_save.save_with_member_fun("file.txt");
    //  save_with_lambda("file.txt");

    // 使用函数包装器封装成一种方式进行调用
    std::function<void(const std::string &)> save1 = save_with_free_fun;
    std::function<void(const std::string &)> save2 = save_with_lambda;
    // 成员函数放入包装器, 只暴露封装后的函数，安全的保护
    std::function<void(const std::string &)> save3 = std::bind(&FileSave::save_with_member_fun, &file_save, std::placeholders::_1);

    //统一的调用方法
    save1("file.txt");
    save2("file.txt");
    save3("file.txt");
    return 0;
}