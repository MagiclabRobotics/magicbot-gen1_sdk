#include "magic_robot.h"
#include "magic_sdk_version.h"

#include <termios.h>
#include <unistd.h>
#include <csignal>

#include <iostream>
#include <chrono>

using namespace magic::gen1;

magic::gen1::MagicRobot robot;

void signalHandler(int signum) {
  std::cout << "Interrupt signal (" << signum << ") received.\n";

  robot.Shutdown();
  // Exit process
  exit(signum);
}

void print_help() {
  std::cout << "Key Function Description:\n";
  std::cout << "Gait and Trick Functions:\n";
  std::cout << "  0        Function 0: Get gait\n";
  std::cout << "  1        Function 1: Set recovery stand gait\n";
  std::cout << "  2        Function 2: Set hybrid gait\n";
  std::cout << "\n";
  std::cout << "Joystick Functions:\n";
  std::cout << "  w        Function w: Move forward\n";
  std::cout << "  a        Function a: Move left\n";
  std::cout << "  s        Function s: Move backward\n";
  std::cout << "  d        Function d: Move right\n";
  std::cout << "  x        Function x: Stop\n";
  std::cout << "  t        Function t: Turn left\n";
  std::cout << "  g        Function g: Turn right\n";
  std::cout << "\n";
  std::cout << "Upper Body Functions:\n";
  std::cout << "  3        Function 3: Subscribe upper body state\n";
  std::cout << "  4        Function 4: Unsubscribe upper body state\n";
  std::cout << "  5        Function 5: Publish upper body command\n";
  std::cout << "  6        Function 6: Subscribe all hand state\n";
  std::cout << "  7        Function 7: Unsubscribe all hand state\n";
  std::cout << "  8        Function 8: Publish all hand command\n";
  std::cout << "\n";
  std::cout << "  ESC      Exit program\n";
  std::cout << "  ?        Function ?: Print help\n";
}

int getch() {
  struct termios oldt, newt;
  int ch;
  tcgetattr(STDIN_FILENO, &oldt);  // Get current terminal settings
  newt = oldt;
  newt.c_lflag &= ~(ICANON | ECHO);  // Disable buffering and echo
  tcsetattr(STDIN_FILENO, TCSANOW, &newt);
  ch = getchar();                           // Read key press
  tcsetattr(STDIN_FILENO, TCSANOW, &oldt);  // Restore settings
  return ch;
}

void GetGait() {
  // Get high-level motion controller
  auto& controller = robot.GetHighLevelMotionController();

  GaitMode gait_mode;
  // Get gait
  auto status = controller.GetGait(gait_mode);
  if (status.code != ErrorCode::OK) {
    std::cerr << "get robot gait failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    return;
  }
  std::cout << "robot gait: " << static_cast<int>(gait_mode) << std::endl;
}

void SetRecoveryStandGait() {
  // Get high-level motion controller
  auto& controller = robot.GetHighLevelMotionController();

  // Set gait
  auto status = controller.SetGait(GaitMode::GAIT_RECOVERY_STAND, 10000);
  if (status.code != ErrorCode::OK) {
    std::cerr << "set robot gait failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    return;
  }
  std::cout << "robot gait set to GAIT_RECOVERY_STAND successfully." << std::endl;
}

void SetHybridGait() {
  // Get high-level motion controller
  auto& controller = robot.GetHighLevelMotionController();

  // Set gait
  auto status = controller.SetGait(GaitMode::GAIT_HYBRID_SDK, 10000);
  if (status.code != ErrorCode::OK) {
    std::cerr << "set robot gait failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    return;
  }
  std::cout << "robot gait set to GAIT_HYBRID_SDK successfully." << std::endl;
}

void JoyStickCommand(float left_x_axis,
                     float left_y_axis,
                     float right_x_axis,
                     float right_y_axis) {
  // Get high-level motion controller
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
  // Wait 50ms
  usleep(50000);
}

void SubscribeUpperBodyState() {
  // Get upper body motion controller
  auto& controller = robot.GetUpperBodyMotionController();

  // Subscribe to upper body state
  controller.SubscribeUpperBodyState([](const std::shared_ptr<JointState> msg) {
    std::cout << "upper body state timestamp: " << msg->timestamp << std::endl;
    for (int ii = 0; ii < msg->joints.size(); ii++) {
      std::cout << "upper body state joint " << ii << " status_word: " << msg->joints[ii].status_word << std::endl;
      std::cout << "upper body state joint " << ii << " posH: " << msg->joints[ii].posH << ", posL: " << msg->joints[ii].posL << std::endl;
      std::cout << "upper body state joint " << ii << " vel: " << msg->joints[ii].vel << ", toq: " << msg->joints[ii].toq << std::endl;
      std::cout << "upper body state joint " << ii << " current: " << msg->joints[ii].current << ", err_code: " << msg->joints[ii].err_code << std::endl;
    }
    std::cout << "--------------------------------" << std::endl;
  });
}

void UnsubscribeUpperBodyState() {
  // Get upper body motion controller
  auto& controller = robot.GetUpperBodyMotionController();

  // Unsubscribe from upper body state
  controller.UnsubscribeUpperBodyState();
}

void PublishUpperBodyCommand() {
  // Get upper body motion controller
  auto& controller = robot.GetUpperBodyMotionController();

  JointCommand command;
  command.timestamp = std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
  command.motion_mode = 1;
  command.joints.resize(18);
  static double pos = 0.0;
  // pos += 0.001;
  for (int ii = 0; ii < 18; ii++) {
    command.joints[ii].operation_mode = 4;
    command.joints[ii].pos = pos;
    command.joints[ii].vel = 0.0;
    command.joints[ii].toq = 0.0;
    command.joints[ii].kp = 0.0;
    command.joints[ii].kd = 0.0;
  }

  command.joints[0].pos = 0.01;
  command.joints[1].pos = 0.11;
  command.joints[2].pos = 1.18;
  command.joints[3].pos = -0.51;
  command.joints[4].pos = -1.49;
  command.joints[5].pos = 0.0;
  command.joints[6].pos = 0.0;

  command.joints[7].pos = 0.01;
  command.joints[8].pos = -0.11;
  command.joints[9].pos = -1.18;
  command.joints[10].pos = 0.51;
  command.joints[11].pos = 1.49;
  command.joints[12].pos = 0.0;
  command.joints[13].pos = 0.0;

  command.joints[14].pos = 0.0;
  command.joints[15].pos = 0.0;
  command.joints[16].pos = 0.0;
  command.joints[17].pos = 0.0;

  command.joints[0].kp = 5.0;
  command.joints[0].kd = 40.0;
  command.joints[1].kp = 5.0;
  command.joints[1].kd = 40.0;

  command.joints[2].kp = 10.0;
  command.joints[2].kd = 25.0;
  command.joints[3].kp = 10.0;
  command.joints[3].kd = 25.0;
  command.joints[4].kp = 10.0;
  command.joints[4].kd = 25.0;
  command.joints[5].kp = 10.0;
  command.joints[5].kd = 25.0;
  command.joints[6].kp = 10.0;
  command.joints[6].kd = 25.0;

  command.joints[7].kp = 5.0;
  command.joints[7].kd = 40.0;
  command.joints[8].kp = 5.0;
  command.joints[8].kd = 40.0;

  command.joints[9].kp = 10.0;
  command.joints[9].kd = 25.0;
  command.joints[10].kp = 10.0;
  command.joints[10].kd = 25.0;
  command.joints[11].kp = 10.0;
  command.joints[11].kd = 25.0;
  command.joints[12].kp = 10.0;
  command.joints[12].kd = 25.0;
  command.joints[13].kp = 10.0;
  command.joints[13].kd = 25.0;

  command.joints[14].kp = 50.0;
  command.joints[14].kd = 200.0;
  command.joints[15].kp = 50.0;
  command.joints[15].kd = 200.0;

  command.joints[16].kp = 250.0;
  command.joints[16].kd = 10.0;
  command.joints[17].kp = 250.0;
  command.joints[17].kd = 10.0;

  // Publish upper body command
  auto status = controller.PublishUpperBodyCommand(command);
  if (status.code != ErrorCode::OK) {
    std::cerr << "publish upper body command failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    return;
  }
  std::cout << status.message << std::endl;
}

void SubscribeAllHandState() {
  // Get upper body motion controller
  auto& controller = robot.GetUpperBodyMotionController();

  // Subscribe to all hand state
  controller.SubscribeAllHandState([](const std::shared_ptr<AllHandState> msg) {
    std::cout << "all hand state timestamp: " << msg->timestamp << std::endl;
    for (int ii = 0; ii < msg->state.size(); ii++) {
      for (int jj = 0; jj < msg->state[ii].status_word.size(); jj++) {
        std::cout << "all hand state hand " << ii << " status_word " << jj << ": " << msg->state[ii].status_word[jj] << std::endl;
      }
      for (int jj = 0; jj < msg->state[ii].pos.size(); jj++) {
        std::cout << "all hand state hand " << ii << " pos " << jj << ": " << msg->state[ii].pos[jj] << std::endl;
      }
      for (int jj = 0; jj < msg->state[ii].toq.size(); jj++) {
        std::cout << "all hand state hand " << ii << " toq " << jj << ": " << msg->state[ii].toq[jj] << std::endl;
      }
      for (int jj = 0; jj < msg->state[ii].cur.size(); jj++) {
        std::cout << "all hand state hand " << ii << " cur " << jj << ": " << msg->state[ii].cur[jj] << std::endl;
      }
      for (int jj = 0; jj < msg->state[ii].error_code.size(); jj++) {
        std::cout << "all hand state hand " << ii << " error_code " << jj << ": " << msg->state[ii].error_code[jj] << std::endl;
      }
    }
    std::cout << "--------------------------------" << std::endl;
  });
}

void UnsubscribeAllHandState() {
  // Get upper body motion controller
  auto& controller = robot.GetUpperBodyMotionController();

  // Unsubscribe from all hand state
  controller.UnsubscribeAllHandState();
}

void PublishAllHandCommand() {
  // Get upper body motion controller
  auto& controller = robot.GetUpperBodyMotionController();

  HandCommand command;
  command.timestamp = std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
  command.cmd.resize(kHandNum);
  static double pos = 0.0;
  // pos += 0.001;
  for (int ii = 0; ii < kHandNum; ii++) {
    command.cmd[ii].operation_mode = 4;
    command.cmd[ii].pos.resize(kHandJointNum);
    for (int jj = 0; jj < kHandJointNum; jj++) {
      command.cmd[ii].pos[jj] = pos;
    }
  } 

  if (kHandNum >= 2 && kHandJointNum >= 6) {
    command.cmd[0].pos[0] = 2.77;
    command.cmd[0].pos[1] = 2.77;
    command.cmd[0].pos[2] = 2.77;
    command.cmd[0].pos[3] = 2.77;
    command.cmd[0].pos[4] = 0.77;
    command.cmd[0].pos[5] = 2.81;

    command.cmd[1].pos[0] = 2.77;
    command.cmd[1].pos[1] = 2.77;
    command.cmd[1].pos[2] = 2.77;
    command.cmd[1].pos[3] = 2.77;
    command.cmd[1].pos[4] = 0.77;
    command.cmd[1].pos[5] = 2.81;
  }

  // Publish all hand command
  controller.PublishAllHandCommand(command);
}

int main(int argc, char* argv[]) {
  // Bind SIGINT (Ctrl+C)
  signal(SIGINT, signalHandler);

  std::cout << "SDK Version: " << SDK_VERSION_STRING << std::endl;

  print_help();

  // std::string local_ip = "192.168.54.111";
  std::string local_ip = "127.0.0.1";
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

  std::cout << "Press any key to continue (ESC to exit)..."
            << std::endl;

  // Wait for user input
  while (1) {
    int key = getch();
    if (key == 27)
      break;  // ESC key ASCII code is 27

    std::cout << "Key ASCII: " << key << ", Character: " << static_cast<char>(key) << std::endl;
    switch (key) {
      // 1. Gait and Trick Functions
      case '0': {
        GetGait();
        break;
      }
      case '1': {
        SetRecoveryStandGait();
        break;
      }
      case '2': {
        SetHybridGait();
        break;
      }
      // 2. Joystick Functions
      case 'w':
      case 'W': {
        JoyStickCommand(0.0, 1.0, 0.0, 0.0);  // Forward
        break;
      }
      case 'a':
      case 'A': {
        JoyStickCommand(-1.0, 0.0, 0.0, 0.0);  // Left
        break;
      }
      case 's':
      case 'S': {
        JoyStickCommand(0.0, -1.0, 0.0, 0.0);  // Backward
        break;
      }
      case 'd':
      case 'D': {
        JoyStickCommand(1.0, 0.0, 0.0, 0.0);  // Right
        break;
      }
      case 'x':
      case 'X': {
        JoyStickCommand(0.0, 0.0, 0.0, 0.0);  // Stop
        break;
      }
      case 't':
      case 'T': {
        JoyStickCommand(0.0, 0.0, -1.0, 0.0);  // Turn left
        break;
      }
      case 'g':
      case 'G': {
        JoyStickCommand(0.0, 0.0, 1.0, 0.0);  // Turn right
        break;
      }
      // 3. Upper Body Functions
      case '3': {
        SubscribeUpperBodyState();
        break;
      }
      case '4': {
        UnsubscribeUpperBodyState();
        break;
      }
      case '5': {
        PublishUpperBodyCommand();
        break;
      }
      case '6': {
        SubscribeAllHandState();
        break;
      }
      case '7': {
        UnsubscribeAllHandState();
        break;
      }
      case '8': {
        PublishAllHandCommand();
        break;
      }
      case '?': {
        print_help();
        break;
      }
      default:
        std::cout << "Unknown key: " << key << std::endl;
        break;
    }
    usleep(10000);
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