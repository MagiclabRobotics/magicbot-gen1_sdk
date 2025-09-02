#pragma once

#include <atomic>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "magic_export.h"
#include "magic_type.h"

#include "magic_audio.h"
#include "magic_motion.h"
#include "magic_sensor.h"
#include "magic_state_monitor.h"

namespace magic::gen1 {
using namespace motion;
using namespace sensor;
using namespace audio;
using namespace monitor;

/**
 * @class MagicRobot
 * @brief Provides a unified management interface for the robot system, including initialization, connection management, access to various sub-controllers, etc.
 *
 * This class is the core entry point of the robot system, responsible for initializing resources, managing communication connections, obtaining robot status,
 * and providing external access to high-level/low-level controllers, audio controllers, and sensor controllers through a unified interface.
 */
class MAGIC_EXPORT_API MagicRobot final : public NonCopyable {
 public:
  /**
   * @brief Constructor, creates a MagicRobot instance.
   */
  MagicRobot();

  /**
   * @brief Destructor, releases MagicRobot instance resources.
   */
  ~MagicRobot();

  /**
   * @brief Initialize the robot system, including controllers, network and other sub-modules.
   * @param local_ip Local IP address for communication binding or identity identification.
   * @return Whether initialization was successful.
   */
  bool Initialize(const std::string& local_ip);

  /**
   * @brief Shutdown the robot system and release resources.
   */
  void Shutdown();

  /**
   * @brief Release the robot system and release resources.
   */
  void Release();

  /**
   * @brief Establish communication connection with robot service.
   * @return gRPC call status, returns Status::OK on success.
   */
  Status Connect();

  /**
   * @brief Disconnect from robot service.
   * @return gRPC call status.
   */
  Status Disconnect();

  /**
   * @brief Get SDK version number.
   * @return Current SDK version string, e.g. "1.2.3".
   */
  std::string GetSDKVersion() const;

  /**
   * @brief Set timeout for interface calls.
   * @param timeout Timeout time in milliseconds. Default timeout is 5000ms.
   */
  void SetTimeout(int timeout);

  /**
   * @brief Get current motion control level.
   * @return Current control mode (high-level control or low-level control).
   */
  ControllerLevel GetMotionControlLevel();

  /**
   * @brief Set motion control level (high-level or low-level).
   * @param level Enum type control level.
   * @return Setting result status.
   */
  Status SetMotionControlLevel(ControllerLevel level);

  /**
   * @brief Get high-level motion controller object.
   * @return Reference type for users to call high-level motion control interfaces.
   */
  HighLevelMotionController& GetHighLevelMotionController();

  /**
   * @brief Get low-level motion controller object.
   * @return Reference type for users to control specific joints/components.
   */
  LowLevelMotionController& GetLowLevelMotionController();

  /**
   * @brief Get audio controller object.
   * @return Reference type for playing speech, adjusting volume, etc.
   */
  AudioController& GetAudioController();

  /**
   * @brief Get sensor controller object.
   * @return Reference type for accessing battery, IMU, camera and other sensor data.
   */
  SensorController& GetSensorController();

  /**
   * @brief Get state monitor object.
   * @return Reference type for obtaining current robot status information.
   */
  StateMonitor& GetStateMonitor();

 private:
  std::atomic_bool is_shutdown_{true};  // Flag indicating whether initialized
};
}  // namespace magic::gen1