#pragma once

#include "magic_export.h"
#include "magic_type.h"

#include <atomic>
#include <functional>
#include <memory>
#include <string>

namespace magic::gen1::sensor {

class SensorController;
using SensorControllerPtr = std::unique_ptr<SensorController>;

/**
 * @class SensorController
 * @brief Sensor controller class that encapsulates initialization, on/off and data acquisition interfaces for various robot sensors.
 *
 * Supports obtaining IMU, point cloud, RGBD images, trinocular camera images and other information, providing unified access methods
 * for upper-level controllers or state fusion modules to call.
 */
class MAGIC_EXPORT_API SensorController final : public NonCopyable {
  // Message pointer type definitions (smart pointers for memory management)
  using PointCloudPtr = std::shared_ptr<PointCloud2>;                   // Point cloud message pointer
  using ImuPtr = std::shared_ptr<Imu>;                                  // IMU inertial measurement unit message pointer
  using ImagePtr = std::shared_ptr<Image>;                              // Image message pointer
  using CameraInfoPtr = std::shared_ptr<CameraInfo>;                    // Camera intrinsic parameter information pointer
  using TrinoculatrCameraPtr = std::shared_ptr<TrinocularCameraFrame>;  // Trinocular camera frame data pointer (spelling suggestion: Trinocular)

  // Various sensor data callback function type definitions
  using LidarImuCallback = std::function<void(const ImuPtr)>;                       // LiDAR IMU data callback
  using LidarPointCloudCallback = std::function<void(const PointCloudPtr)>;         // LiDAR point cloud data callback
  using RgbdImageCallback = std::function<void(const ImagePtr)>;                    // RGBD image data callback
  using RgbdCameraInfoCallback = std::function<void(const CameraInfoPtr)>;          // RGBD camera intrinsic parameter callback
  using TrinocularImageCallback = std::function<void(const TrinoculatrCameraPtr)>;  // Trinocular camera image frame callback

 public:
  /// Constructor: Create SensorController instance, initialize internal state
  SensorController();

  /// Destructor: Release resources, close all sensors
  virtual ~SensorController();

  /**
   * @brief Initialize sensor controller, including resource application, driver loading, etc.
   * @return Returns true on successful initialization, false otherwise.
   */
  bool Initialize();

  /**
   * @brief Close all sensor connections and release resources.
   */
  void Shutdown();

  // === LiDAR Control ===

  /**
   * @brief Open LiDAR.
   * @return Operation status.
   */
  Status OpenLidar();

  /**
   * @brief Close LiDAR.
   * @return Operation status.
   */
  Status CloseLidar();

  // === RGBD Camera Control ===

  /**
   * @brief Open head RGBD camera (including head and waist).
   * @return Operation status.
   */
  Status OpenHeadRgbdCamera();

  /**
   * @brief Close head RGBD camera.
   * @return Operation status.
   */
  Status CloseHeadRgbdCamera();

  /**
   * @brief Open waist RGBD camera (including head and waist).
   * @return Operation status.
   */
  Status OpenWaistRgbdCamera();

  /**
   * @brief Close waist RGBD camera.
   * @return Operation status.
   */
  Status CloseWaistRgbdCamera();

  // === Trinocular Camera Control ===

  /**
   * @brief Open trinocular camera.
   * @return Operation status.
   */
  Status OpenTrinocularCamera();

  /**
   * @brief Close trinocular camera.
   * @return Operation status.
   */
  Status CloseTrinocularCamera();

  // Function interfaces for subscribing to various sensor data

  /**
   * @brief Subscribe to LiDAR IMU data
   * @param callback Processing callback after receiving LiDAR IMU data
   */
  void SubscribeLidarImu(const LidarImuCallback callback);

  /**
   * @brief Unsubscribe from LiDAR IMU data
   */
  void UnsubscribeLidarImu();

  /**
   * @brief Subscribe to LiDAR point cloud data
   * @param callback Processing callback after receiving point cloud data
   */
  void SubscribeLidarPointCloud(const LidarPointCloudCallback callback);

  /**
   * @brief Unsubscribe from LiDAR point cloud data
   */
  void UnsubscribeLidarPointCloud();

  /**
   * @brief Subscribe to head RGBD color image data
   * @param callback Processing callback after receiving image data
   */
  void SubscribeHeadRgbdColorImage(const RgbdImageCallback callback);

  /**
   * @brief Unsubscribe from head RGBD color image data
   */
  void UnsubscribeHeadRgbdColorImage();

  /**
   * @brief Subscribe to head RGBD color camera parameter data
   * @param callback Processing callback after receiving camera information
   */
  void SubscribeHeadRgbdColorCameraInfo(const RgbdCameraInfoCallback callback);

  /**
   * @brief Unsubscribe from head RGBD color camera parameter data
   */
  void UnsubscribeHeadRgbdColorCameraInfo();

  /**
   * @brief Subscribe to head RGBD depth image data
   * @param callback Processing callback after receiving depth image data
   */
  void SubscribeHeadRgbdDepthImage(const RgbdImageCallback callback);

  /**
   * @brief Unsubscribe from head RGBD depth image data
   */
  void UnsubscribeHeadRgbdDepthImage();

  /**
   * @brief Subscribe to head RGBD depth camera parameter data
   * @param callback Processing callback after receiving depth camera information
   */
  void SubscribeHeadRgbdDepthCameraInfo(const RgbdCameraInfoCallback callback);

  /**
   * @brief Unsubscribe from head RGBD depth camera parameter data
   */
  void UnsubscribeHeadRgbdDepthCameraInfo();

  /**
   * @brief Subscribe to waist RGBD color image data
   * @param callback Processing callback after receiving image data
   */
  void SubscribeWaistRgbdColorImage(const RgbdImageCallback callback);

  /**
   * @brief Unsubscribe from waist RGBD color image data
   */
  void UnsubscribeWaistRgbdColorImage();

  /**
   * @brief Subscribe to waist RGBD color camera parameter data
   * @param callback Processing callback after receiving camera information
   */
  void SubscribeWaistRgbdColorCameraInfo(const RgbdCameraInfoCallback callback);

  /**
   * @brief Unsubscribe from waist RGBD color camera parameter data
   */
  void UnsubscribeWaistRgbdColorCameraInfo();

  /**
   * @brief Subscribe to waist RGBD depth image data
   * @param callback Processing callback after receiving depth image data
   */
  void SubscribeWaistRgbdDepthImage(const RgbdImageCallback callback);

  /**
   * @brief Unsubscribe from waist RGBD depth image data
   */
  void UnsubscribeWaistRgbdDepthImage();

  /**
   * @brief Subscribe to waist RGBD depth camera parameter data
   * @param callback Processing callback after receiving depth camera information
   */
  void SubscribeWaistRgbdDepthCameraInfo(const RgbdCameraInfoCallback callback);

  /**
   * @brief Unsubscribe from waist RGBD depth camera parameter data
   */
  void UnsubscribeWaistRgbdDepthCameraInfo();

  /**
   * @brief Subscribe to trinocular camera image frame data
   * @param callback Processing callback after receiving trinocular camera data
   */
  void SubscribeTrinocularImage(const TrinocularImageCallback callback);

  /**
   * @brief Unsubscribe from trinocular camera image frame data
   */
  void UnsubscribeTrinocularImage();

 private:
  std::atomic_bool is_shutdown_{true};  // Flag indicating whether initialized
};

}  // namespace magic::gen1::sensor
