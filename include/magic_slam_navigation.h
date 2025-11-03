#pragma once

#include "magic_export.h"
#include "magic_type.h"

#include <atomic>
#include <functional>
#include <memory>
#include <string>

namespace magic::gen1::slam {

class SlamNavController;
using SlamNavControllerPtr = std::unique_ptr<SlamNavController>;

class MAGIC_EXPORT_API SlamNavController final : public NonCopyable {
  using LocalizationInfoPtr = std::shared_ptr<LocalizationInfo>;
  using OdometryCallback = std::function<void(const std::shared_ptr<Odometry>)>;
  using PointCloudMapCallback = std::function<void(const std::shared_ptr<PointCloud2>)>;

 public:
  /**
   * @brief Constructor, creates a SlamNavController instance.
   */
  SlamNavController();

  /**
   * @brief Destructor, releases SlamNavController instance resources.
   */
  ~SlamNavController();

  /**
   * @brief Initialize SLAM controller.
   * @return Whether initialization was successful.
   */
  bool Initialize();

  /**
   * @brief Release resources, clean up SLAM controller.
   */
  void Shutdown();

  /**
   * @brief activate slam mode and start mapping or localization mode
   * @param mode Mode to switch to, such as idle mode/localization mode/mapping mode, etc.
   * @param map_path Map path, when mode is localization mode, map_path is the path of the map to be reused, such as: "/home/eame/cust_para/maps/${map_name}/${map_date}."
   * @param timeout_ms Timeout in milliseconds, default is 10000
   * @return Operation status, returns Status::OK on success
   */
  Status ActivateSlamMode(SlamMode mode, std::string map_path = "", int timeout_ms = 10000);

  /**
   * @brief Start mapping
   * @param timeout_ms Timeout in milliseconds, default is 10000
   * @return Operation status, returns Status::OK on success
   */
  Status StartMapping(int timeout_ms = 10000);

  /**
   * @brief Cancel mapping
   * @param timeout_ms Timeout in milliseconds, default is 10000
   * @return Operation status, returns Status::OK on success
   */
  Status CancelMapping(int timeout_ms = 10000);

  /**
   * @brief End mapping and save map, when in mapping mode
   * @param map_name Map name
   * @param timeout_ms Timeout in milliseconds, default is 10000
   * @return Operation status, returns Status::OK on success
   */
  Status SaveMap(const std::string& map_name, int timeout_ms = 10000);

  /**
   * @brief load map and set as the current map
   * @param map_name Map name
   * @param timeout_ms Timeout in milliseconds, default is 10000
   * @return Operation status, returns Status::OK on success
   */
  Status LoadMap(const std::string& map_name, int timeout_ms = 10000);

  /**
   * @brief Delete map
   * @param map_name Name of the map to delete
   * @param timeout_ms Timeout in milliseconds, default is 10000
   * @return Operation status, returns Status::OK on success
   */
  Status DeleteMap(const std::string& map_name, int timeout_ms = 10000);

  /**
   * @brief Get map path
   * @param map_name Map name
   * @param map_path Map path. such as: "/home/eame/cust_para/maps/${map_name}/${map_date}."
   * @param timeout_ms Timeout in milliseconds, default is 10000
   * @return Operation status, returns Status::OK on success
   */
  Status GetMapPath(const std::string& map_name, std::vector<std::string>& map_path, int timeout_ms = 10000);

  /**
   * @brief Get all map information
   * @param all_map_info All map information (output parameter)
   * @param timeout_ms Timeout in milliseconds, default is 10000
   * @return Operation status, returns Status::OK on success
   */
  Status GetAllMapInfo(AllMapInfo& all_map_info, int timeout_ms = 10000);

  /**
   * @brief Initialize pose
   * @param pose Pose information to publish. Due to the lidar being installed with a -1.57rad offset relative to the robot's front, the desired yaw orientation needs to be offset by -1.57rad, otherwise the robot's pose initialization may fail
   * @param timeout_ms Timeout in milliseconds, default is 15000
   * @return Operation status, returns Status::OK on success
   */
  Status InitPose(Pose3DEuler& pose, int timeout_ms = 10000);

  /**
   * @brief Get current pose information
   * @param pose_info Current position and attitude information (output parameter)
   * @return Operation status, returns Status::OK on success
   */
  Status GetCurrentLocalizationInfo(LocalizationInfo& pose_info);

  /**
   * @brief activate navigation mode
   * @param mode Target navigation mode (NavigationMode enumeration type)
   * @param map_path Map path, when mode is GRID_MAP mode, map_path is the path of the map to be reused
   * @param timeout_ms Timeout in milliseconds, default is 10000
   * @return Operation status, returns Status::OK on success
   */
  Status ActivateNavMode(NavMode mode, std::string map_path = "", int timeout_ms = 10000);

  /**
   * @brief Set global navigation target point and start navigation task
   * @param goal Global coordinates of the target point
   * @param timeout_ms Timeout in milliseconds, default is 10000
   * @return Operation status, returns Status::OK on success
   */
  Status SetNavTarget(const NavTarget& goal, int timeout_ms = 10000);

  /**
   * @brief Pause current navigation task
   * @param timeout_ms Timeout in milliseconds
   * @return Operation status, returns Status::OK on success
   */
  Status PauseNavTask();

  /**
   * @brief Resume paused navigation task
   * @param timeout_ms Timeout in milliseconds
   * @return Operation status, returns Status::OK on success
   */
  Status ResumeNavTask();

  /**
   * @brief Cancel current navigation task
   * @param timeout_ms Timeout in milliseconds
   * @return Operation status, returns Status::OK on success
   */
  Status CancelNavTask();

  /**
   * @brief Get navigation task status
   * @param nav_status Navigation task status (output parameter)
   * @param timeout_ms Timeout in milliseconds
   * @return Operation status, returns Status::OK on success
   */
  Status GetNavTaskStatus(NavStatus& nav_status);

  /**
   * @brief Open odometry stream
   * @return Operation status, returns Status::OK on success
   */
  Status OpenOdometryStream();

  /**
   * @brief Close odometry stream
   * @return Operation status, returns Status::OK on success
   */
  Status CloseOdometryStream();

  /**
   * @brief Subscribe to odometry data
   * @param callback Processing callback after receiving odometry data
   */
  void SubscribeOdometry(const OdometryCallback callback);

  /**
   * @brief Unsubscribe from odometry data
   */
  void UnsubscribeOdometry();

  /**
   * @brief Get point cloud map
   * @param point_cloud_map Point cloud map (output parameter)
   * @param timeout_ms Timeout in milliseconds, default is 10000
   * @return Operation status, returns Status::OK on success
   */
  Status GetPointCloudMap(PointCloud2& point_cloud_map, int timeout_ms = 10000);

 private:
  std::atomic_bool is_shutdown_{true};  // Mark whether it has been initialized
};

}  // namespace magic::gen1::slam