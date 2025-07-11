#include "magic_robot.h"

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

int main() {
  // 绑定 SIGINT（Ctrl+C）
  signal(SIGINT, signalHandler);

  std::string local_ip = "192.168.54.111";
  // 配置本机网线直连机器的IP地址，并进行SDK初始化
  if (!robot.Initialize(local_ip)) {
    std::cerr << "robot sdk initialize failed." << std::endl;
    robot.Shutdown();
    return -1;
  }

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
  status = robot.SetMotionControlLevel(ControllerLevel::LowLevel);
  if (status.code != ErrorCode::OK) {
    std::cerr << "switch robot motion control level failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    robot.Shutdown();
    return -1;
  }

  // 获取底层控制器
  auto& controller = robot.GetLowLevelMotionController();

  // 设置控制指令发送周期为2ms，500HZ
  controller.SetPeriodMs(2);

  // 订阅imu数据
  controller.SubscribeBodyImu([](const std::shared_ptr<Imu> msg) {
    static int32_t count = 0;
    if (count++ % 1000 == 1) {
      std::cout << "receive imu data." << std::endl;
    }
    // TODO: handle imu data
  });

  // 订阅手部数据
  controller.SubscribeArmState([](const std::shared_ptr<JointState> msg) {
    static int32_t count = 0;
    if (count++ % 1000 == 1) {
      std::cout << "receive arm joint data." << std::endl;
    }
    // TODO: handle arm joint data
  });

  // 以上臂关节控制为例：

  // 第一次发布手部控制指令，关节的操作模式为200，表示关节处于准备状态
  {
    JointCommand arm_command;
    arm_command.joints.resize(kArmJointNum);
    for (int ii = 0; ii < kArmJointNum; ii++) {
      arm_command.joints[ii].operation_mode = 200;
    }
    controller.PublishArmCommand(arm_command);
  }

  // 后续关节控制指令，关节的操作模式为1，表示关节处于位置控制模式
  {
    // 左臂关节，参考文档：
    // 左臂或者右臂1-5关节operation_mode需要从模式：200切换到模式：4（串联PID模式）进行指令下发；
    JointCommand arm_command;
    arm_command.joints.resize(kArmJointNum);
    for (int ii = 0; ii < 5; ii++) {
      arm_command.joints[ii].operation_mode = 4;
      // TODO:设置目标位置、速度、力矩和增益
    }

    for (int ii = 5; ii < 6; ii++) {
      arm_command.joints[ii].operation_mode = 5;
      // TODO:设置目标位置、速度、力矩和增益
    }

    for (int ii = 7; ii < 12; ii++) {
      arm_command.joints[ii].operation_mode = 4;
      // TODO:设置目标位置、速度、力矩和增益
    }

    for (int ii = 12; ii < 13; ii++) {
      arm_command.joints[ii].operation_mode = 5;
      // TODO:设置目标位置、速度、力矩和增益
    }
    controller.PublishArmCommand(arm_command);
  }

  usleep(100000000);

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