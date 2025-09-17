#include "magic_robot.h"
#include "magic_type.h"

#include <unistd.h>
#include <csignal>

#include <iostream>

using namespace magic::gen1;

magic::gen1::MagicRobot robot;

void signalHandler(int signum) {
  std::cout << "Interrupt signal (" << signum << ") received.\n";

  robot.Shutdown();
  // Exit process
  exit(signum);
}

int main() {
  // Bind SIGINT (Ctrl+C)
  signal(SIGINT, signalHandler);

  std::string local_ip = "192.168.54.111";
  // Configure local IP address for direct network connection and initialize SDK
  if (!robot.Initialize(local_ip)) {
    std::cerr << "robot sdk initialize failed." << std::endl;
    robot.Shutdown();
    return -1;
  }

  // Connect to robot
  auto status = robot.Connect();
  if (status.code != ErrorCode::OK) {
    std::cerr << "connect robot failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    robot.Shutdown();
    return -1;
  }

  auto& controller = robot.GetSensorController();

  // Open LiDAR
  status = controller.OpenLidar();
  if (status.code != ErrorCode::OK) {
    std::cerr << "open lidar failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    robot.Shutdown();
    return -1;
  }

  // Subscribe to LiDAR IMU data
  controller.SubscribeLidarImu([](const std::shared_ptr<Imu> msg) {
    std::cout << "receive lidar imu." << std::endl;
    // TODO: handle lidar imu data
  });

  // Subscribe to LiDAR PointCloud data
  controller.SubscribeLidarPointCloud([](const std::shared_ptr<PointCloud2> msg) {
    std::cout << "receive lidar point cloud." << std::endl;
    // TODO: handle lidar point cloud data
  });

  usleep(20000000);

  // Close LiDAR
  status = controller.CloseLidar();
  if (status.code != ErrorCode::OK) {
    std::cerr << "close lidar failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    robot.Shutdown();
    return -1;
  }

  // Disconnect from robot
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