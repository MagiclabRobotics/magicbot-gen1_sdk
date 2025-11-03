#include "magic_robot.h"
#include "magic_sdk_version.h"
#include "magic_type.h"

#include <termios.h>
#include <unistd.h>
#include <csignal>

#include <atomic>
#include <iostream>
#include <map>
#include <memory>
#include <string>

using namespace magic::gen1;

// Global counters for periodic logging
std::atomic<int> lidar_imu_counter{0};
std::atomic<int> lidar_pointcloud_counter{0};
std::atomic<int> head_rgbd_color_counter{0};
std::atomic<int> head_rgbd_depth_counter{0};
std::atomic<int> waist_rgbd_color_counter{0};
std::atomic<int> waist_rgbd_depth_counter{0};
std::atomic<int> trinocular_image_counter{0};

class SensorManager {
 public:
  explicit SensorManager(SensorController& controller)
      : sensor_controller_(controller) {
    sensors_state_["lidar"] = false;
    sensors_state_["head_rgbd_camera"] = false;
    sensors_state_["waist_rgbd_camera"] = false;
    sensors_state_["trinocular_camera"] = false;

    subscriptions_["lidar_imu"] = false;
    subscriptions_["lidar_point_cloud"] = false;
    subscriptions_["head_rgbd_color_image"] = false;
    subscriptions_["head_rgbd_depth_image"] = false;
    subscriptions_["waist_rgbd_color_image"] = false;
    subscriptions_["waist_rgbd_depth_image"] = false;
    subscriptions_["trinocular_image"] = false;
  }

  // === LiDAR Control ===
  bool OpenLidar() {
    if (sensors_state_["lidar"]) {
      std::cout << "[WARNING] LiDAR already opened" << std::endl;
      return true;
    }

    auto status = sensor_controller_.OpenLidar();
    if (status.code != ErrorCode::OK) {
      std::cerr << "[ERROR] Failed to open LiDAR: " << status.message << std::endl;
      return false;
    }

    sensors_state_["lidar"] = true;
    std::cout << "[INFO] ✓ LiDAR opened successfully" << std::endl;
    return true;
  }

  bool CloseLidar() {
    if (!sensors_state_["lidar"]) {
      std::cout << "[WARNING] LiDAR already closed" << std::endl;
      return true;
    }

    // Unsubscribe if subscribed
    if (subscriptions_["lidar_imu"]) ToggleLidarImuSubscription();
    if (subscriptions_["lidar_point_cloud"]) ToggleLidarPointCloudSubscription();

    auto status = sensor_controller_.CloseLidar();
    if (status.code != ErrorCode::OK) {
      std::cerr << "[ERROR] Failed to close LiDAR: " << status.message << std::endl;
      return false;
    }

    sensors_state_["lidar"] = false;
    std::cout << "[INFO] ✓ LiDAR closed" << std::endl;
    return true;
  }

  // === Head RGBD Camera Control ===
  bool OpenHeadRgbdCamera() {
    if (sensors_state_["head_rgbd_camera"]) {
      std::cout << "[WARNING] Head RGBD camera already opened" << std::endl;
      return true;
    }

    auto status = sensor_controller_.OpenHeadRgbdCamera();
    if (status.code != ErrorCode::OK) {
      std::cerr << "[ERROR] Failed to open head RGBD camera: " << status.message << std::endl;
      return false;
    }

    sensors_state_["head_rgbd_camera"] = true;
    std::cout << "[INFO] ✓ Head RGBD camera opened" << std::endl;
    return true;
  }

  bool CloseHeadRgbdCamera() {
    if (!sensors_state_["head_rgbd_camera"]) {
      std::cout << "[WARNING] Head RGBD camera already closed" << std::endl;
      return true;
    }

    if (subscriptions_["head_rgbd_color_image"]) ToggleHeadRgbdColorImageSubscription();
    if (subscriptions_["head_rgbd_depth_image"]) ToggleHeadRgbdDepthImageSubscription();

    auto status = sensor_controller_.CloseHeadRgbdCamera();
    if (status.code != ErrorCode::OK) {
      std::cerr << "[ERROR] Failed to close head RGBD camera: " << status.message << std::endl;
      return false;
    }

    sensors_state_["head_rgbd_camera"] = false;
    std::cout << "[INFO] ✓ Head RGBD camera closed" << std::endl;
    return true;
  }

  // === Waist RGBD Camera Control ===
  bool OpenWaistRgbdCamera() {
    if (sensors_state_["waist_rgbd_camera"]) {
      std::cout << "[WARNING] Waist RGBD camera already opened" << std::endl;
      return true;
    }

    auto status = sensor_controller_.OpenWaistRgbdCamera();
    if (status.code != ErrorCode::OK) {
      std::cerr << "[ERROR] Failed to open waist RGBD camera: " << status.message << std::endl;
      return false;
    }

    sensors_state_["waist_rgbd_camera"] = true;
    std::cout << "[INFO] ✓ Waist RGBD camera opened" << std::endl;
    return true;
  }

  bool CloseWaistRgbdCamera() {
    if (!sensors_state_["waist_rgbd_camera"]) {
      std::cout << "[WARNING] Waist RGBD camera already closed" << std::endl;
      return true;
    }

    if (subscriptions_["waist_rgbd_color_image"]) ToggleWaistRgbdColorImageSubscription();
    if (subscriptions_["waist_rgbd_depth_image"]) ToggleWaistRgbdDepthImageSubscription();

    auto status = sensor_controller_.CloseWaistRgbdCamera();
    if (status.code != ErrorCode::OK) {
      std::cerr << "[ERROR] Failed to close waist RGBD camera: " << status.message << std::endl;
      return false;
    }

    sensors_state_["waist_rgbd_camera"] = false;
    std::cout << "[INFO] ✓ Waist RGBD camera closed" << std::endl;
    return true;
  }

  // === Trinocular Camera Control ===
  bool OpenTrinocularCamera() {
    if (sensors_state_["trinocular_camera"]) {
      std::cout << "[WARNING] Trinocular camera already opened" << std::endl;
      return true;
    }

    auto status = sensor_controller_.OpenTrinocularCamera();
    if (status.code != ErrorCode::OK) {
      std::cerr << "[ERROR] Failed to open trinocular camera: " << status.message << std::endl;
      return false;
    }

    sensors_state_["trinocular_camera"] = true;
    std::cout << "[INFO] ✓ Trinocular camera opened" << std::endl;
    return true;
  }

  bool CloseTrinocularCamera() {
    if (!sensors_state_["trinocular_camera"]) {
      std::cout << "[WARNING] Trinocular camera already closed" << std::endl;
      return true;
    }

    if (subscriptions_["trinocular_image"]) ToggleTrinocularImageSubscription();

    auto status = sensor_controller_.CloseTrinocularCamera();
    if (status.code != ErrorCode::OK) {
      std::cerr << "[ERROR] Failed to close trinocular camera: " << status.message << std::endl;
      return false;
    }

    sensors_state_["trinocular_camera"] = false;
    std::cout << "[INFO] ✓ Trinocular camera closed" << std::endl;
    return true;
  }

  // === LiDAR Subscriptions ===
  void ToggleLidarImuSubscription() {
    if (subscriptions_["lidar_imu"]) {
      sensor_controller_.UnsubscribeLidarImu();
      subscriptions_["lidar_imu"] = false;
      std::cout << "[INFO] ✓ LiDAR IMU unsubscribed" << std::endl;
    } else {
      sensor_controller_.SubscribeLidarImu([](const std::shared_ptr<Imu> msg) {
        lidar_imu_counter++;
        if (lidar_imu_counter % 100 == 0) {
          std::cout << "[DATA] LiDAR IMU received (count: " << lidar_imu_counter << ")" << std::endl;
        }
      });
      subscriptions_["lidar_imu"] = true;
      std::cout << "[INFO] ✓ LiDAR IMU subscribed" << std::endl;
    }
  }

  void ToggleLidarPointCloudSubscription() {
    if (subscriptions_["lidar_point_cloud"]) {
      sensor_controller_.UnsubscribeLidarPointCloud();
      subscriptions_["lidar_point_cloud"] = false;
      std::cout << "[INFO] ✓ LiDAR point cloud unsubscribed" << std::endl;
    } else {
      sensor_controller_.SubscribeLidarPointCloud([](const std::shared_ptr<PointCloud2> msg) {
        lidar_pointcloud_counter++;
        if (lidar_pointcloud_counter % 10 == 0) {
          std::cout << "[DATA] LiDAR Point Cloud: " << msg->data.size()
                    << " bytes (count: " << lidar_pointcloud_counter << ")" << std::endl;
        }
      });
      subscriptions_["lidar_point_cloud"] = true;
      std::cout << "[INFO] ✓ LiDAR point cloud subscribed" << std::endl;
    }
  }

  // === Head RGBD Subscriptions ===
  void ToggleHeadRgbdColorImageSubscription() {
    if (subscriptions_["head_rgbd_color_image"]) {
      sensor_controller_.UnsubscribeHeadRgbdColorImage();
      subscriptions_["head_rgbd_color_image"] = false;
      std::cout << "[INFO] ✓ Head RGBD color image unsubscribed" << std::endl;
    } else {
      sensor_controller_.SubscribeHeadRgbdColorImage([](const std::shared_ptr<Image> msg) {
        head_rgbd_color_counter++;
        if (head_rgbd_color_counter % 15 == 0) {
          std::cout << "[DATA] Head RGBD Color Image: " << msg->data.size()
                    << " bytes, " << msg->width << "x" << msg->height
                    << " (count: " << head_rgbd_color_counter << ")" << std::endl;
        }
      });
      subscriptions_["head_rgbd_color_image"] = true;
      std::cout << "[INFO] ✓ Head RGBD color image subscribed" << std::endl;
    }
  }

  void ToggleHeadRgbdDepthImageSubscription() {
    if (subscriptions_["head_rgbd_depth_image"]) {
      sensor_controller_.UnsubscribeHeadRgbdDepthImage();
      subscriptions_["head_rgbd_depth_image"] = false;
      std::cout << "[INFO] ✓ Head RGBD depth image unsubscribed" << std::endl;
    } else {
      sensor_controller_.SubscribeHeadRgbdDepthImage([](const std::shared_ptr<Image> msg) {
        head_rgbd_depth_counter++;
        if (head_rgbd_depth_counter % 15 == 0) {
          std::cout << "[DATA] Head RGBD Depth Image: " << msg->data.size()
                    << " bytes, " << msg->width << "x" << msg->height
                    << " (count: " << head_rgbd_depth_counter << ")" << std::endl;
        }
      });
      subscriptions_["head_rgbd_depth_image"] = true;
      std::cout << "[INFO] ✓ Head RGBD depth image subscribed" << std::endl;
    }
  }

  // === Waist RGBD Subscriptions ===
  void ToggleWaistRgbdColorImageSubscription() {
    if (subscriptions_["waist_rgbd_color_image"]) {
      sensor_controller_.UnsubscribeWaistRgbdColorImage();
      subscriptions_["waist_rgbd_color_image"] = false;
      std::cout << "[INFO] ✓ Waist RGBD color image unsubscribed" << std::endl;
    } else {
      sensor_controller_.SubscribeWaistRgbdColorImage([](const std::shared_ptr<Image> msg) {
        waist_rgbd_color_counter++;
        if (waist_rgbd_color_counter % 15 == 0) {
          std::cout << "[DATA] Waist RGBD Color Image: " << msg->data.size()
                    << " bytes, " << msg->width << "x" << msg->height
                    << " (count: " << waist_rgbd_color_counter << ")" << std::endl;
        }
      });
      subscriptions_["waist_rgbd_color_image"] = true;
      std::cout << "[INFO] ✓ Waist RGBD color image subscribed" << std::endl;
    }
  }

  void ToggleWaistRgbdDepthImageSubscription() {
    if (subscriptions_["waist_rgbd_depth_image"]) {
      sensor_controller_.UnsubscribeWaistRgbdDepthImage();
      subscriptions_["waist_rgbd_depth_image"] = false;
      std::cout << "[INFO] ✓ Waist RGBD depth image unsubscribed" << std::endl;
    } else {
      sensor_controller_.SubscribeWaistRgbdDepthImage([](const std::shared_ptr<Image> msg) {
        waist_rgbd_depth_counter++;
        if (waist_rgbd_depth_counter % 15 == 0) {
          std::cout << "[DATA] Waist RGBD Depth Image: " << msg->data.size()
                    << " bytes, " << msg->width << "x" << msg->height
                    << " (count: " << waist_rgbd_depth_counter << ")" << std::endl;
        }
      });
      subscriptions_["waist_rgbd_depth_image"] = true;
      std::cout << "[INFO] ✓ Waist RGBD depth image subscribed" << std::endl;
    }
  }

  // === Trinocular Camera Subscriptions ===
  void ToggleTrinocularImageSubscription() {
    if (subscriptions_["trinocular_image"]) {
      sensor_controller_.UnsubscribeTrinocularImage();
      subscriptions_["trinocular_image"] = false;
      std::cout << "[INFO] ✓ Trinocular camera image unsubscribed" << std::endl;
    } else {
      sensor_controller_.SubscribeTrinocularImage([](const std::shared_ptr<TrinocularCameraFrame> msg) {
        trinocular_image_counter++;
        if (trinocular_image_counter % 15 == 0) {
          std::cout << "[DATA] Trinocular Camera Frame received (count: "
                    << trinocular_image_counter << ")" << std::endl;
        }
      });
      subscriptions_["trinocular_image"] = true;
      std::cout << "[INFO] ✓ Trinocular camera image subscribed" << std::endl;
    }
  }

  void ShowStatus() {
    std::cout << "\n"
              << std::string(80, '=') << std::endl;
    std::cout << "MAGICBOT GEN1 SENSOR STATUS" << std::endl;
    std::cout << std::string(80, '=') << std::endl;
    std::cout << "LiDAR:                         " << (sensors_state_["lidar"] ? "OPEN" : "CLOSED") << std::endl;
    std::cout << "Head RGBD Camera:              " << (sensors_state_["head_rgbd_camera"] ? "OPEN" : "CLOSED") << std::endl;
    std::cout << "Waist RGBD Camera:             " << (sensors_state_["waist_rgbd_camera"] ? "OPEN" : "CLOSED") << std::endl;
    std::cout << "Trinocular Camera:             " << (sensors_state_["trinocular_camera"] ? "OPEN" : "CLOSED") << std::endl;
    std::cout << "\nLIDAR SUBSCRIPTIONS:" << std::endl;
    std::cout << "  LiDAR IMU:                   " << (subscriptions_["lidar_imu"] ? "✓ SUBSCRIBED" : "✗ UNSUBSCRIBED") << std::endl;
    std::cout << "  LiDAR Point Cloud:           " << (subscriptions_["lidar_point_cloud"] ? "✓ SUBSCRIBED" : "✗ UNSUBSCRIBED") << std::endl;
    std::cout << "\nHEAD RGBD SUBSCRIPTIONS:" << std::endl;
    std::cout << "  Color Image:                 " << (subscriptions_["head_rgbd_color_image"] ? "✓ SUBSCRIBED" : "✗ UNSUBSCRIBED") << std::endl;
    std::cout << "  Depth Image:                 " << (subscriptions_["head_rgbd_depth_image"] ? "✓ SUBSCRIBED" : "✗ UNSUBSCRIBED") << std::endl;
    std::cout << "\nWAIST RGBD SUBSCRIPTIONS:" << std::endl;
    std::cout << "  Color Image:                 " << (subscriptions_["waist_rgbd_color_image"] ? "✓ SUBSCRIBED" : "✗ UNSUBSCRIBED") << std::endl;
    std::cout << "  Depth Image:                 " << (subscriptions_["waist_rgbd_depth_image"] ? "✓ SUBSCRIBED" : "✗ UNSUBSCRIBED") << std::endl;
    std::cout << "\nTRINOCULAR CAMERA SUBSCRIPTIONS:" << std::endl;
    std::cout << "  Trinocular Image:            " << (subscriptions_["trinocular_image"] ? "✓ SUBSCRIBED" : "✗ UNSUBSCRIBED") << std::endl;
    std::cout << std::string(80, '=') << "\n"
              << std::endl;
  }

  void CleanupAll() {
    if (sensors_state_["lidar"]) CloseLidar();
    if (sensors_state_["head_rgbd_camera"]) CloseHeadRgbdCamera();
    if (sensors_state_["waist_rgbd_camera"]) CloseWaistRgbdCamera();
    if (sensors_state_["trinocular_camera"]) CloseTrinocularCamera();
  }

 private:
  SensorController& sensor_controller_;
  std::map<std::string, bool> sensors_state_;
  std::map<std::string, bool> subscriptions_;
};

void PrintMenu() {
  std::cout << "\n"
            << std::string(80, '=') << std::endl;
  std::cout << "MAGICBOT GEN1 SENSOR CONTROL MENU" << std::endl;
  std::cout << std::string(80, '=') << std::endl;
  std::cout << "Sensor Open/Close:" << std::endl;
  std::cout << "  1 - Open LiDAR                     2 - Close LiDAR" << std::endl;
  std::cout << "  3 - Open Head RGBD Camera          4 - Close Head RGBD Camera" << std::endl;
  std::cout << "  5 - Open Waist RGBD Camera         6 - Close Waist RGBD Camera" << std::endl;
  std::cout << "  7 - Open Trinocular Camera         8 - Close Trinocular Camera" << std::endl;
  std::cout << "\nLiDAR Subscriptions:" << std::endl;
  std::cout << "  i - Toggle LiDAR IMU               p - Toggle LiDAR Point Cloud" << std::endl;
  std::cout << "\nHead RGBD Camera Subscriptions:" << std::endl;
  std::cout << "  c - Toggle Head Color Image        d - Toggle Head Depth Image" << std::endl;
  std::cout << "\nWaist RGBD Camera Subscriptions:" << std::endl;
  std::cout << "  w - Toggle Waist Color Image       e - Toggle Waist Depth Image" << std::endl;
  std::cout << "\nTrinocular Camera Subscriptions:" << std::endl;
  std::cout << "  t - Toggle Trinocular Image" << std::endl;
  std::cout << "\nCommands:" << std::endl;
  std::cout << "  s - Show Status                    ESC - Exit program      ? - Help" << std::endl;
  std::cout << std::string(80, '=') << std::endl;
}

magic::gen1::MagicRobot robot;
SensorManager* g_sensor_manager = nullptr;

void signalHandler(int signum) {
  std::cout << "\n[INFO] Interrupt signal (" << signum << ") received.\n";

  if (g_sensor_manager) {
    std::cout << "[INFO] Cleaning up..." << std::endl;
    g_sensor_manager->CleanupAll();
  }

  robot.Shutdown();
  exit(signum);
}

int main() {
  // Bind SIGINT (Ctrl+C)
  signal(SIGINT, signalHandler);

  std::cout << "\n"
            << std::string(80, '=') << std::endl;
  std::cout << "MagicBot Gen1 SDK Sensor Interactive Example" << std::endl;
  std::cout << "SDK Version: " << SDK_VERSION_STRING << std::endl;
  std::cout << std::string(80, '=') << "\n"
            << std::endl;

  std::string local_ip = "192.168.54.111";

  // Initialize SDK
  if (!robot.Initialize(local_ip)) {
    std::cerr << "[ERROR] Robot SDK initialize failed." << std::endl;
    robot.Shutdown();
    return -1;
  }

  // Connect to robot
  auto status = robot.Connect();
  if (status.code != ErrorCode::OK) {
    std::cerr << "[ERROR] Connect robot failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
    robot.Shutdown();
    return -1;
  }

  std::cout << "[INFO] ✓ Robot connected successfully\n"
            << std::endl;

  auto& controller = robot.GetSensorController();
  SensorManager sensor_manager(controller);
  g_sensor_manager = &sensor_manager;

  PrintMenu();

  try {
    std::string choice;
    while (true) {
      std::cout << "\nEnter your choice: ";
      std::getline(std::cin, choice);

      if (choice.empty()) continue;

      char cmd = choice[0];

      // ESC key command
      if (cmd == 27) {
        std::cout << "[INFO] ESC key pressed, exiting program..." << std::endl;
        break;
      }

      // Sensor open/close control
      switch (cmd) {
        case '1':
          sensor_manager.OpenLidar();
          break;
        case '2':
          sensor_manager.CloseLidar();
          break;
        case '3':
          sensor_manager.OpenHeadRgbdCamera();
          break;
        case '4':
          sensor_manager.CloseHeadRgbdCamera();
          break;
        case '5':
          sensor_manager.OpenWaistRgbdCamera();
          break;
        case '6':
          sensor_manager.CloseWaistRgbdCamera();
          break;
        case '7':
          sensor_manager.OpenTrinocularCamera();
          break;
        case '8':
          sensor_manager.CloseTrinocularCamera();
          break;

        // LiDAR subscriptions
        case 'i':
          sensor_manager.ToggleLidarImuSubscription();
          break;
        case 'p':
          sensor_manager.ToggleLidarPointCloudSubscription();
          break;

        // Head RGBD subscriptions
        case 'c':
          sensor_manager.ToggleHeadRgbdColorImageSubscription();
          break;
        case 'd':
          sensor_manager.ToggleHeadRgbdDepthImageSubscription();
          break;

        // Waist RGBD subscriptions
        case 'w':
          sensor_manager.ToggleWaistRgbdColorImageSubscription();
          break;
        case 'e':
          sensor_manager.ToggleWaistRgbdDepthImageSubscription();
          break;

        // Trinocular camera subscriptions
        case 't':
          sensor_manager.ToggleTrinocularImageSubscription();
          break;

        // Commands
        case 's':
        case 'S':
          sensor_manager.ShowStatus();
          break;
        case '?':
          PrintMenu();
          break;

        default:
          std::cout << "[WARNING] Invalid choice: '" << choice << "'. Press '?' for help." << std::endl;
          break;
      }
    }
  } catch (const std::exception& e) {
    std::cerr << "[ERROR] Exception occurred: " << e.what() << std::endl;
  }

  // Cleanup
  std::cout << "[INFO] Cleaning up..." << std::endl;
  sensor_manager.CleanupAll();

  sleep(1);  // Allow time for cleanup

  // Disconnect from robot
  status = robot.Disconnect();
  if (status.code != ErrorCode::OK) {
    std::cerr << "[ERROR] Disconnect robot failed"
              << ", code: " << status.code
              << ", message: " << status.message << std::endl;
  } else {
    std::cout << "[INFO] Robot disconnected" << std::endl;
  }

  robot.Shutdown();
  std::cout << "[INFO] Robot shutdown" << std::endl;

  return 0;
}