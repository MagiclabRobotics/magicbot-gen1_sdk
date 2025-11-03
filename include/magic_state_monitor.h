#pragma once

#include "magic_export.h"
#include "magic_type.h"

#include <atomic>
#include <memory>
#include <string>

namespace magic::gen1::monitor {

class StateMonitor;
using StateMonitorPtr = std::unique_ptr<StateMonitor>;

/**
 * @class StateMonitor
 * @brief Class that encapsulates state control functionality, providing state query and other interfaces.
 *
 * This class is typically used for state management of robots or smart devices, supporting state query and initialization,
 * and providing resource release mechanisms.
 */

class MAGIC_EXPORT_API StateMonitor final : public NonCopyable {
 public:
  /**
   * @brief Constructor, creates a StateMonitor instance.
   */
  StateMonitor();

  /**
   * @brief Destructor, releases StateMonitor instance resources.
   */
  ~StateMonitor();

  /**
   * @brief Initialize state controller.
   * @return Whether initialization was successful.
   */
  bool Initialize();

  /**
   * @brief Release resources, clean up state controller.
   */
  void Shutdown();

  /**
   * @brief Get current robot running state (aggregated state information).
   * @return robot_state for receiving current robot state.
   */
  Status GetCurrentState(RobotState& robot_state);

 private:
  std::atomic_bool is_shutdown_{true};  // Flag indicating whether initialized
};

}  // namespace magic::gen1::monitor