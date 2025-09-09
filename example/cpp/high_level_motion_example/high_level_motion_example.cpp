#include "magic_robot.h"

#include <termios.h>
#include <unistd.h>
#include <csignal>

#include <iostream>

using namespace magic::gen1;

magic::gen1::MagicRobot robot;

void signalHandler(int signum) {
  std::cout << "Interrupt signal (" << signum << ") received.\n";

  robot.Shutdown();
  // 退出进程
  exit(signum);
}

void print_help(const char* prog_name) {
  std::cout << "按键功能演示程序\n\n";
  std::cout << "用法: " << prog_name << "\n";
  std::cout << "按键功能说明:\n";
  std::cout << "  ESC      退出程序\n";
  std::cout << "  1        功能1:锁定站立\n";
  std::cout << "  2        功能2:平衡站立\n";
  std::cout << "  3        功能3:执行特技-庆祝动作\n";
  std::cout << "  w        功能4:向前移动\n";
  std::cout << "  a        功能5:向左移动\n";
  std::cout << "  s        功能6:向后移动\n";
  std::cout << "  d        功能7:向右移动\n";
  std::cout << "  x        功能8:向右移动\n";
  std::cout << "  t        功能9:左转向\n";
  std::cout << "  g        功能10:右转向\n";
}

int getch() {
  struct termios oldt, newt;
  int ch;
  tcgetattr(STDIN_FILENO, &oldt);  // 获取当前终端设置
  newt = oldt;
  newt.c_lflag &= ~(ICANON | ECHO);  // 关闭缓冲和回显
  tcsetattr(STDIN_FILENO, TCSANOW, &newt);
  ch = getchar();                           // 读取按键
  tcsetattr(STDIN_FILENO, TCSANOW, &oldt);  // 恢复设置
  return ch;
}

void RecoveryStand() {
  // 获取高层运控控制器
  auto& controller = robot.GetHighLevelMotionController();

  // 设置步态
  auto status = controller.SetGait(GaitMode::GAIT_RECOVERY_STAND);
  if (status.code != ErrorCode::OK) {
    std::cerr << "set robot gait failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    return;
  }
}

void BalanceStand() {
  // 获取高层运控控制器
  auto& controller = robot.GetHighLevelMotionController();

  // 设置姿态展示步态
  auto status = controller.SetGait(GaitMode::GAIT_BALANCE_STAND);
  if (status.code != ErrorCode::OK) {
    std::cerr << "set robot gait failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    return;
  }
  std::cout << "robot gait set to GAIT_BALANCE_STAND successfully." << std::endl;
}

void ExecuteTrick() {
  // 获取高层运控控制器
  auto& controller = robot.GetHighLevelMotionController();

  // 执行特技
  auto status = controller.ExecuteTrick(TrickAction::ACTION_CELEBRATE);
  if (status.code != ErrorCode::OK) {
    std::cerr << "execute robot trick failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    return;
  }
  std::cout << "robot trick executed successfully." << std::endl;
}

void JoyStickCommand(float left_x_axis,
                     float left_y_axis,
                     float right_x_axis,
                     float right_y_axis) {
  // 获取高层运控控制器
  auto& controller = robot.GetHighLevelMotionController();

  JoystickCommand joy_command;
  joy_command.left_x_axis = left_x_axis;
  joy_command.left_y_axis = left_y_axis;
  joy_command.right_x_axis = right_x_axis;
  joy_command.right_y_axis = right_y_axis;
  auto status = controller.SendJoyStickCommand(joy_command);
  if (status.code != ErrorCode::OK) {
    std::cerr << "execute robot trick failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    usleep(50000);
    return;
  }
  // 等待50ms
  usleep(50000);
}

int main(int argc, char* argv[]) {
  // 绑定 SIGINT（Ctrl+C）
  signal(SIGINT, signalHandler);

  std::string local_ip = "192.168.54.111";
  // 配置本机网线直连机器的IP地址，并进行SDK初始化
  if (!robot.Initialize(local_ip)) {
    std::cerr << "robot sdk initialize failed." << std::endl;
    robot.Shutdown();
    return -1;
  }

  // Set RPC timeout to 10s
  robot.SetTimeout(10000);

  // 连接机器人
  auto status = robot.Connect();
  if (status.code != ErrorCode::OK) {
    std::cerr << "connect robot failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    robot.Shutdown();
    return -1;
  }

  // 切换运控控制器为底层控制器，默认是高层控制器
  status = robot.SetMotionControlLevel(ControllerLevel::HighLevel);
  if (status.code != ErrorCode::OK) {
    std::cerr << "switch robot motion control level failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    robot.Shutdown();
    return -1;
  }

  std::cout << "按任意键继续 (ESC退出)..."
            << std::endl;

  // 等待用户输入
  while (1) {
    int key = getch();
    if (key == 27)
      break;  // ESC键ASCII码为27

    std::cout << "按键ASCII: " << key << ", 字符: " << static_cast<char>(key) << std::endl;
    switch (key) {
      case '1': {
        RecoveryStand();
        break;
      }
      case '2': {
        BalanceStand();
        break;
      }
      case '3': {
        ExecuteTrick();
        break;
      }
      case 'w': {
        JoyStickCommand(0.0, 1.0, 0.0, 0.0);  // 向前
        break;
      }
      case 'a': {
        JoyStickCommand(-1.0, 0.0, 0.0, 0.0);  // 向左
        break;
      }
      case 's': {
        JoyStickCommand(0.0, -1.0, 0.0, 0.0);  // 向后
        break;
      }
      case 'd': {
        JoyStickCommand(1.0, 0.0, 0.0, 0.0);  // 向右
        break;
      }
      case 'x': {
        JoyStickCommand(0.0, 0.0, 0.0, 0.0);  // 停止
        break;
      }
      case 't': {
        JoyStickCommand(0.0, 0.0, -1.0, 0.0);  // 左转
        break;
      }
      case 'g': {
        JoyStickCommand(0.0, 0.0, 1.0, 0.0);  // 右转
        break;
      }
      default:
        std::cout << "未知按键: " << key << std::endl;
        break;
    }
    usleep(10000);
  }

  // 断开与机器人的链接
  status = robot.Disconnect();
  if (status.code != ErrorCode::OK) {
    std::cerr << "disconnect robot failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    robot.Shutdown();
    return -1;
  }

  robot.Shutdown();

  return 0;
}