#include "magic_robot.h"

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

  // Set control command sending period to 2ms, 500Hz
  controller.SetPeriodMs(2);

  // Subscribe to IMU data
  controller.SubscribeBodyImu([](const std::shared_ptr<Imu> msg) {
    static int32_t count = 0;
    if (count++ % 1000 == 1) {
      std::cout << "receive imu data." << std::endl;
    }
    // TODO: handle imu data
  });

  // Subscribe to arm data
  controller.SubscribeArmState([](const std::shared_ptr<JointState> msg) {
    static int32_t count = 0;
    if (count++ % 1000 == 1) {
      std::cout << "receive arm joint data." << std::endl;
    }
    // TODO: handle arm joint data
  });

  // Take arm joint control as an example:

  // First publish arm control command, joint operation mode is 200, indicating joint is in preparation state
  {
    JointCommand arm_command;
    arm_command.joints.resize(kArmJointNum);
    for (int ii = 0; ii < kArmJointNum; ii++) {
      arm_command.joints[ii].operation_mode = 200;
    }
    controller.PublishArmCommand(arm_command);
  }

  // Subsequent joint control commands, joint operation mode is 1, indicating joint is in position control mode
  {
    // Left arm joints, refer to documentation:
    // Left arm or right arm joints 1-5 operation_mode needs to switch from mode: 200 to mode: 4 (series PID mode) for command sending;
    JointCommand arm_command;
    arm_command.joints.resize(kArmJointNum);
    for (int ii = 0; ii < 5; ii++) {
      arm_command.joints[ii].operation_mode = 4;
      // TODO: Set target position, velocity, torque and gains
    }

    for (int ii = 5; ii < 6; ii++) {
      arm_command.joints[ii].operation_mode = 5;
      // TODO: Set target position, velocity, torque and gains
    }

    for (int ii = 7; ii < 12; ii++) {
      arm_command.joints[ii].operation_mode = 4;
      // TODO: Set target position, velocity, torque and gains
    }

    for (int ii = 12; ii < 13; ii++) {
      arm_command.joints[ii].operation_mode = 5;
      // TODO: Set target position, velocity, torque and gains
    }
    controller.PublishArmCommand(arm_command);
  }

  usleep(100000000);

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