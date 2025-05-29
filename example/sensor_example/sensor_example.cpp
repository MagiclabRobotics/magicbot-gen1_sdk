#include "magic_robot.h"
#include "magic_type.h"

#include <unistd.h>
#include <csignal>

#include <iostream>

using namespace magic::robot;

magic::robot::MagicRobot robot;

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

  // 设置rpc超时时间为5s
  robot.SetTimeout(5000);

  // 连接机器人
  auto status = robot.Connect();
  if (status.code != ErrorCode::OK) {
    std::cerr << "connect robot failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    robot.Shutdown();
    return -1;
  }

  auto& controller = robot.GetSensorController();

  // 打开lidar
  status = controller.OpenLidar();
  if (status.code != ErrorCode::OK) {
    std::cerr << "open lidar failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    robot.Shutdown();
    return -1;
  }

  // 订阅Lidar Imu数据
  controller.SubscribeLidarImu([](const std::shared_ptr<Imu> msg) {
    std::cout << "receive lidar imu." << std::endl;
    // TODO: handle lidar imu data
  });

  // 订阅Lidar PointCloud数据
  controller.SubscribeLidarPointCloud([](const std::shared_ptr<PointCloud2> msg) {
    std::cout << "receive lidar point cloud." << std::endl;
    // TODO: handle lidar point cloud data
  });

  usleep(50000000);

  // 关闭lidar
  status = controller.CloseLidar();
  if (status.code != ErrorCode::OK) {
    std::cerr << "close lidar failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    robot.Shutdown();
    return -1;
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