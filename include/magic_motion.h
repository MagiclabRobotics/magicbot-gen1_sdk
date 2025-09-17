#pragma once

#include "magic_export.h"
#include "magic_type.h"

#include <atomic>
#include <functional>
#include <memory>
#include <string>

namespace magic::gen1::motion {

class LowLevelMotionController;
using LowLevelMotionControllerPtr = std::unique_ptr<LowLevelMotionController>;

class HighLevelMotionController;
using HighLevelMotionControllerPtr = std::unique_ptr<HighLevelMotionController>;

/**
 * @brief Abstract base class defining common interfaces for robot motion controllers.
 *
 * MotionControllerBase is the base class for all motion controllers, providing pure virtual function interfaces
 * for initializing and shutting down controllers. Derived classes must implement these interfaces to meet specific control requirements.
 */
class MAGIC_EXPORT_API MotionControllerBase : public NonCopyable {
 public:
  /**
   * @brief Constructor.
   */
  MotionControllerBase() = default;

  /**
   * @brief Virtual destructor, ensures proper resource release in derived classes.
   */
  virtual ~MotionControllerBase() = default;

  /**
   * @brief Initialize controller.
   * @return Returns true on successful initialization, false otherwise.
   */
  virtual bool Initialize() = 0;

  /**
   * @brief Shutdown controller, release related resources.
   */
  virtual void Shutdown() = 0;

 protected:
  std::atomic_bool is_shutdown_{true};  // Flag indicating whether initialized
};

/**
 * @class HighLevelMotionController
 * @brief High-level motion controller for semantic-level action control of robots (such as: walking, tricks, head movements, etc.).
 *
 * This class inherits from MotionControllerBase, mainly targeting high-level user interfaces, hiding underlying details.
 */
class MAGIC_EXPORT_API HighLevelMotionController final : public MotionControllerBase {
 public:
  /// Constructor, initializes high-level controller internal state.
  HighLevelMotionController();

  /// Destructor, releases resources.
  virtual ~HighLevelMotionController();

  /**
   * @brief Initialize controller, prepare high-level control functionality.
   * @return Whether initialization was successful.
   */
  virtual bool Initialize() override;

  /**
   * @brief Shutdown controller, release related resources.
   */
  virtual void Shutdown() override;

  /**
   * @brief Set robot gait mode (such as recovery stand, balance stand, humanoid walk, etc., refer to GaitMode definition).
   * @param gait_mode Enum type gait mode.
   * @param timeout_ms Timeout in milliseconds.
   * @return Execution status.
   */
  Status SetGait(const GaitMode gait_mode, int timeout_ms = 10000);

  /**
   * @brief Get robot gait mode (such as recovery stand, balance stand, humanoid walk, etc., refer to GaitMode definition).
   * @param gait_mode Enum type gait mode.
   * @return Execution status.
   */
  Status GetGait(GaitMode& gait_mode);

  /**
   * @brief Execute specified trick action (such as bowing, waving, etc.).
   * @param trick_action Trick action identifier.
   * @param timeout_ms Timeout in milliseconds.
   * @return Execution status.
   * @note Trick actions are usually predefined complex action sequences, must be performed under GaitMode::GAIT_BALANCE_STAND(46) gait for trick display.
   */
  Status ExecuteTrick(const TrickAction trick_action, int timeout_ms = 10000);

  /**
   * @brief Send real-time joystick control command. Recommended sending frequency is 20Hz.
   * @param joy_command Control command containing left and right joystick coordinates.
   * @return Execution status.
   */
  Status SendJoyStickCommand(JoystickCommand& joy_command);
};

/**
 * @class LowLevelMotionController
 * @brief Low-level motion controller, directly controls joint movements of various motion components (such as arms, legs, head, waist, etc.).
 *
 * Targets low-level developers or control systems, providing command sending and status reading interfaces for various body components.
 */
class MAGIC_EXPORT_API LowLevelMotionController final : public MotionControllerBase {
  // Message pointer type definitions (smart pointers for memory management)
  using JointStatePtr = std::shared_ptr<JointState>;  // Joint state message pointer
  using HandStatePtr = std::shared_ptr<HandState>;    // Hand state message pointer
  using ImuPtr = std::shared_ptr<Imu>;                // IMU inertial measurement unit message pointer

  // Various joint data callback function type definitions
  using ArmJointStateCallback = std::function<void(const JointStatePtr)>;    // Arm joint state callback function type
  using LegJointStateCallback = std::function<void(const JointStatePtr)>;    // Leg joint state callback function type
  using HeadJointStateCallback = std::function<void(const JointStatePtr)>;   // Head joint state callback function type
  using WaistJointStateCallback = std::function<void(const JointStatePtr)>;  // Waist joint state callback function type
  using HandStateCallback = std::function<void(const HandStatePtr)>;         // Hand state callback function type
  using BodyImuCallback = std::function<void(const ImuPtr)>;                 // Body IMU data callback

 public:
  /// Constructor, initializes low-level controller.
  LowLevelMotionController();

  /// Destructor, releases resources.
  virtual ~LowLevelMotionController();

  /**
   * @brief Initialize controller, establish low-level motion control connection.
   * @return Whether initialization was successful.
   */
  virtual bool Initialize() override;

  /**
   * @brief Shutdown controller, release low-level resources.
   */
  virtual void Shutdown() override;

  // === Arm Control ===

  /**
   * @brief Subscribe to arm joint state data
   * @param callback Callback function for processing received arm joint state data
   */
  void SubscribeArmState(ArmJointStateCallback callback);

  /**
   * @brief Publish arm joint control command
   * @param command Arm joint control command containing target angle/velocity and other control information
   * @return Execution status.
   */
  Status PublishArmCommand(const JointCommand& command);

  // === Leg Control ===

  /**
   * @brief Subscribe to leg joint state data
   * @param callback Callback function for processing received leg joint state data
   */
  void SubscribeLegState(LegJointStateCallback callback);

  /**
   * @brief Publish leg joint control command
   * @param command Leg joint control command containing target angle/velocity and other control information
   * @return Execution status.
   */
  Status PublishLegCommand(const JointCommand& command);

  // === Head Control ===

  /**
   * @brief Subscribe to head joint state data
   * @param callback Callback function for processing received head joint state data
   */
  void SubscribeHeadState(HeadJointStateCallback callback);

  /**
   * @brief Publish head joint control command
   * @param command Head joint control command containing target angle/velocity and other control information
   * @return Execution status.
   */
  Status PublishHeadCommand(const JointCommand& command);

  // === Waist Control ===

  /**
   * @brief Subscribe to waist joint state data
   * @param callback Callback function for processing received waist joint state data
   */
  void SubscribeWaistState(WaistJointStateCallback callback);

  /**
   * @brief Publish waist joint control command
   * @param command Waist joint control command containing target angle/velocity and other control information
   * @return Execution status.
   */
  Status PublishWaistCommand(const JointCommand& command);

  // === Hand Control ===

  /**
   * @brief Subscribe to hand state data (such as gripping state, opening/closing degree, etc.)
   * @param callback Callback function for processing received hand state data
   */
  void SubscribeHandState(HandStateCallback callback);

  /**
   * @brief Publish hand control command
   * @param command Hand control command containing gripper action, force control and other information
   * @return Execution status.
   */
  Status PublishHandCommand(const HandCommand& command);

  /**
   * @brief Subscribe to body IMU data
   * @param callback Processing callback after receiving IMU data
   */
  void SubscribeBodyImu(const BodyImuCallback callback);
};

}  // namespace magic::gen1::motion