#include <QApplication>
#include <QLabel>
#include <QString>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QLabel* label = new QLabel();
    QString msg = QString::fromStdString("Hello Qt!");

    label->setText(msg);
    label->show();
    app.exec();   //执行应用，阻塞代码，直到退出，这里是退出qt界面

    return 0;
}