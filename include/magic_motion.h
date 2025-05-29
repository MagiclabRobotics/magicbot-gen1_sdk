#pragma once

#include "magic_export.h"
#include "magic_type.h"

#include <atomic>
#include <functional>
#include <memory>
#include <string>

namespace magic::robot::motion {

class LowLevelMotionController;
using LowLevelMotionControllerPtr = std::unique_ptr<LowLevelMotionController>;

class HighLevelMotionController;
using HighLevelMotionControllerPtr = std::unique_ptr<HighLevelMotionController>;

/**
 * @brief 抽象基类，定义机器人运动控制器的通用接口。
 *
 * MotionControllerBase 是所有运动控制器的基类，提供初始化和关闭控制器的纯虚函数接口。
 * 派生类需实现这些接口，以满足具体的控制需求。
 */
class MAGIC_EXPORT_API MotionControllerBase : public NonCopyable {
 public:
  /**
   * @brief 构造函数。
   */
  MotionControllerBase() = default;

  /**
   * @brief 虚析构函数，确保派生类资源正确释放。
   */
  virtual ~MotionControllerBase() = default;

  /**
   * @brief 初始化控制器。
   * @return 初始化成功返回 true，否则返回 false。
   */
  virtual bool Initialize() = 0;

  /**
   * @brief 关闭控制器，释放相关资源。
   */
  virtual void Shutdown() = 0;

 protected:
  std::atomic_bool is_shutdown_{true};  // 标记是否已初始化
};

/**
 * @class HighLevelMotionController
 * @brief 高层运动控制器，用于对机器人进行语义层面的动作控制（如：行走、特技、头部运动等）。
 *
 * 该类继承自 MotionControllerBase，主要面向高层用户接口，隐藏底层细节。
 */
class MAGIC_EXPORT_API HighLevelMotionController final : public MotionControllerBase {
 public:
  /// 构造函数，初始化高层控制器内部状态。
  HighLevelMotionController();

  /// 析构函数，释放资源。
  virtual ~HighLevelMotionController();

  /**
   * @brief 初始化控制器，准备高层控制功能。
   * @return 初始化是否成功。
   */
  virtual bool Initialize() override;

  /**
   * @brief 关闭控制器，释放相关资源。
   */
  virtual void Shutdown() override;

  /**
   * @brief 设置机器人的步态模式（如站立锁定、平衡站立、拟人行走等，参考GaitMode定义）。
   * @param gait_mode 枚举类型的步态模式。
   * @return 执行状态。
   */
  Status SetGait(const GaitMode gait_mode);

  /**
   * @brief 获取机器人的步态模式（如站立锁定、平衡站立、拟人行走等，参考GaitMode定义）。
   * @param gait_mode 枚举类型的步态模式。
   * @return 执行状态。
   */
  Status GetGait(GaitMode& gait_mode);

  /**
   * @brief 执行指定的特技动作（如鞠躬、挥手等）。
   * @param trick_action 特技动作标识。
   * @return 执行状态。
   * @note 特技动作通常是预定义的复杂动作序列, 必须要在GaitMode::GAIT_BALANCE_STAND(46)步态下才能进行特技展示。
   */
  Status ExecuteTrick(const TrickAction trick_action);

  /**
   * @brief 发送实时摇杆控制指令。发送频率建议20HZ。
   * @param joy_command 包含左右摇杆坐标的控制指令。
   * @return 执行状态。
   */
  Status SendJoyStickCommand(JoystickCommand& joy_command);
};

/**
 * @class LowLevelMotionController
 * @brief 低层运动控制器，直接控制各个运动部件（如手臂、腿、头、腰等）的关节动作。
 *
 * 面向底层开发者或控制系统，提供各个身体部件的指令下发与状态读取接口。
 */
class MAGIC_EXPORT_API LowLevelMotionController final : public MotionControllerBase {
  // 消息指针类型定义（智能指针，便于内存管理）
  using JointStatePtr = std::shared_ptr<JointState>;  // 关节状态消息指针
  using HandStatePtr = std::shared_ptr<HandState>;    // 手部状态消息指针
  using ImuPtr = std::shared_ptr<Imu>;                // IMU 惯性测量单元消息指针

  // 各类关节数据的回调函数类型定义
  using ArmJointStateCallback = std::function<void(const JointStatePtr)>;    // 手臂关节状态回调函数类型
  using LegJointStateCallback = std::function<void(const JointStatePtr)>;    // 腿部关节状态回调函数类型
  using HeadJointStateCallback = std::function<void(const JointStatePtr)>;   // 头部关节状态回调函数类型
  using WaistJointStateCallback = std::function<void(const JointStatePtr)>;  // 腰部关节状态回调函数类型
  using HandStateCallback = std::function<void(const HandStatePtr)>;         // 手部状态回调函数类型
  using BodyImuCallback = std::function<void(const ImuPtr)>;                 // 机体 IMU 数据的回调

 public:
  /// 构造函数，初始化低层控制器。
  LowLevelMotionController();

  /// 析构函数，释放资源。
  virtual ~LowLevelMotionController();

  /**
   * @brief 初始化控制器，建立底层运动控制连接。
   * @return 初始化是否成功。
   */
  virtual bool Initialize() override;

  /**
   * @brief 关闭控制器，释放底层资源。
   */
  virtual void Shutdown() override;

  /**
   * @brief 设置控制器的周期时间（单位：毫秒）。
   * @param period_ms 控制器周期时间，单位为毫秒。
   * @note 如果设置的周期小于1ms，将自动调整为默认值2ms，建议不低于2ms。
   */
  void SetPeriodMs(uint64_t period_ms);

  // === 手臂控制 ===

  /**
   * @brief 订阅手臂关节状态数据
   * @param callback 回调函数，用于处理手臂关节状态的接收数据
   */
  void SubscribeArmState(ArmJointStateCallback callback);

  /**
   * @brief 发布手臂关节控制指令
   * @param command 包含目标角度/速度等控制信息的手臂关节控制指令
   * @return 执行状态。
   */
  Status PublishArmCommand(const JointCommand& command);

  // === 腿部控制 ===

  /**
   * @brief 订阅腿部关节状态数据
   * @param callback 回调函数，用于处理腿部关节状态的接收数据
   */
  void SubscribeLegState(LegJointStateCallback callback);

  /**
   * @brief 发布腿部关节控制指令
   * @param command 包含目标角度/速度等控制信息的腿部关节控制指令
   * @return 执行状态。
   */
  Status PublishLegCommand(const JointCommand& command);

  // === 头部控制 ===

  /**
   * @brief 订阅头部关节状态数据
   * @param callback 回调函数，用于处理头部关节状态的接收数据
   */
  void SubscribeHeadState(HeadJointStateCallback callback);

  /**
   * @brief 发布头部关节控制指令
   * @param command 包含目标角度/速度等控制信息的头部关节控制指令
   * @return 执行状态。
   */
  Status PublishHeadCommand(const JointCommand& command);

  // === 腰部控制 ===

  /**
   * @brief 订阅腰部关节状态数据
   * @param callback 回调函数，用于处理腰部关节状态的接收数据
   */
  void SubscribeWaistState(WaistJointStateCallback callback);

  /**
   * @brief 发布腰部关节控制指令
   * @param command 包含目标角度/速度等控制信息的腰部关节控制指令
   * @return 执行状态。
   */
  Status PublishWaistCommand(const JointCommand& command);

  // === 手部控制 ===

  /**
   * @brief 订阅手部状态数据（如夹持状态、开合程度等）
   * @param callback 回调函数，用于处理手部状态的接收数据
   */
  void SubscribeHandState(HandStateCallback callback);

  /**
   * @brief 发布手部控制指令
   * @param command 包含夹爪动作、力量控制等信息的手部控制指令
   * @return 执行状态。
   */
  Status PublishHandCommand(const HandCommand& command);

  /**
   * @brief 订阅机体 IMU 数据
   * @param callback 接收到 IMU 数据后的处理回调
   */
  void SubscribeBodyImu(const BodyImuCallback callback);
};

}  // namespace magic::robot::motion