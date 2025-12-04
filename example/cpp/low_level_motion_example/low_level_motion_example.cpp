#include "magic_robot.h"
#include "magic_sdk_version.h"

#include <unistd.h>
#include <atomic>
#include <chrono>
#include <csignal>
#include <iostream>
#include <thread>

using namespace magic::gen1;

magic::gen1::MagicRobot robot;

std::atomic<bool> running(true);

void signalHandler(int signum) {
  std::cout << "Interrupt signal (" << signum << ") received.\n";

  running = false;

  robot.Shutdown();
  // Exit process
  exit(signum);
}

int main() {
  // Bind SIGINT (Ctrl+C)
  signal(SIGINT, signalHandler);

  std::cout << "SDK Version: " << SDK_VERSION_STRING << std::endl;

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

  // Switch motion control controller to low-level controller, default is high-level controller
  status = robot.SetMotionControlLevel(ControllerLevel::LowLevel);
  if (status.code != ErrorCode::OK) {
    std::cerr << "switch robot motion control level failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    robot.Shutdown();
    return -1;
  }

  // Get low-level controller
  auto& controller = robot.GetLowLevelMotionController();

  // Subscribe to IMU data
  controller.SubscribeBodyImu([](const std::shared_ptr<Imu> msg) {
    static int32_t count = 0;
    if (count++ % 1000 == 1) {
      std::cout << "+++++++++++ receive imu data." << std::endl;
      std::cout << "timestamp: " << msg->timestamp << std::endl;
      std::cout << "temperature: " << msg->temperature << std::endl;
      std::cout << "orientation: " << msg->orientation[0] << ", " << msg->orientation[1] << ", " << msg->orientation[2] << ", " << msg->orientation[3] << std::endl;
      std::cout << "angular_velocity: " << msg->angular_velocity[0] << ", " << msg->angular_velocity[1] << ", " << msg->angular_velocity[2] << std::endl;
      std::cout << "linear_acceleration: " << msg->linear_acceleration[0] << ", " << msg->linear_acceleration[1] << ", " << msg->linear_acceleration[2] << std::endl;
    }
    // TODO: handle imu data
  });

  // Subscribe to arm data
  controller.SubscribeArmState([](const std::shared_ptr<JointState> msg) {
    static int32_t count = 0;
    if (count++ % 1000 == 1) {
      std::cout << "+++++++++++ receive arm joint data." << std::endl;
      std::cout << "timestamp: " << msg->timestamp << std::endl;
      std::cout << "pos: " << msg->joints[0].posH << ", " << msg->joints[0].posL << std::endl;
      std::cout << "vel: " << msg->joints[0].vel << std::endl;
      std::cout << "toq: " << msg->joints[0].toq << std::endl;
      std::cout << "current: " << msg->joints[0].current << std::endl;
      std::cout << "error_code: " << msg->joints[0].err_code << std::endl;
    }
    // TODO: handle arm joint data
  });

  // Using arm joint control as an example:
  // Subsequent joint control commands, joint operation mode is 1, indicating the joint is in position control mode
  auto now = std::chrono::steady_clock::now();
  while (running.load()) {
    // Left arm joints, refer to documentation:
    // Left arm or right arm joints 1-5 operation_mode needs to switch from mode: 200 to mode: 4 (series PID mode) for command execution;
    JointCommand arm_command;
    arm_command.joints.resize(kArmJointNum);
    for (int ii = 0; ii < kArmJointNum; ii++) {
      // Set joint to ready state
      arm_command.joints[ii].operation_mode = 200;
      // TODO: Set target position, velocity, torque and gains
      arm_command.joints[ii].pos = 0.0;
      arm_command.joints[ii].vel = 0.0;
      arm_command.joints[ii].toq = 0.0;
      arm_command.joints[ii].kp = 0.0;
      arm_command.joints[ii].kd = 0.0;
    }
    // Publish control command
    controller.PublishArmCommand(arm_command);

    // Send control command at 500Hz frequency (2ms)
    now += std::chrono::milliseconds(2);
    std::this_thread::sleep_until(now);
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