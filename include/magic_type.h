#pragma once

#include <array>
#include <cstdint>
#include <string>
#include <vector>

namespace magic::robot {

/************************************************************
 *                        常量信息                           *
 ************************************************************/

constexpr uint8_t kHandJointNum = 6;
constexpr uint8_t kHandNum = 2;
constexpr uint8_t kHeadJointNum = 2;
constexpr uint8_t kArmJointNum = 14;
constexpr uint8_t kWaistJointNum = 3;
constexpr uint8_t kLegJointNum = 12;

constexpr uint64_t kPeriodMs = 2;  ///< 控制器周期时间，单位为毫秒

/************************************************************
 *                        接口信息                           *
 ************************************************************/

enum ErrorCode {
  OK = 0,
  SERVICE_NOT_READY = 1,
  TIMEOUT = 2,
  INTERNAL_ERROR = 3,
  SERVICE_ERROR = 4,
};

struct Status {
  ErrorCode code;
  std::string message;
};

/************************************************************
 *                        状态信息                           *
 ************************************************************/
/**
 * @brief 错误信息结构体
 *
 * 用于表示系统中发生的错误信息，包括错误代码和错误消息。
 */
struct Fault {
  /**
   * @brief 错误代码
   *
   * 整型值，用于标识具体的异常类型。不同的错误代码可以对应不同的错误类型，便于错误管理和处理。
   */
  int error_code;

  /**
   * @brief 错误信息
   *
   * 描述错误发生的具体信息，通常是对错误原因的详细描述，便于调试和定位问题。
   */
  std::string error_message;
};

/**
 * @brief 电池状态枚举类型
 *
 * 表示电池当前的状态，包含多个可能的电池状态选项，用于系统中电池状态的判断和处理。
 */
enum class BatteryState : int8_t {
  UNKNOWN = 0,                ///< 未知状态
  GOOD = 1,                   ///< 电池状态良好
  OVERHEAT = 2,               ///< 电池过热
  DEAD = 3,                   ///< 电池损坏
  OVERVOLTAGE = 4,            ///< 电池过电压
  UNSPEC_FAILURE = 5,         ///< 未知故障
  COLD = 6,                   ///< 电池过冷
  WATCHDOG_TIMER_EXPIRE = 7,  ///< 看门狗定时器超时
  SAFETY_TIMER_EXPIRE = 8,    ///< 安全定时器超时
};

/**
 * @brief 电池充放电状态
 */
enum class PowerSupplyStatus : int8_t {
  UNKNOWN = 0,      ///< 未知状态
  CHARGING = 1,     ///< 电池充电中
  DISCHARGING = 2,  ///< 电池放电中
  NOTCHARGING = 3,  ///< 电池未充放电
  FULL = 4,         ///< 电池充满
};

/**
 * @brief 电池管理系统数据结构体
 *
 * 用于存储电池的相关信息，包括电池的剩余电量、电池健康状况、电池状态和充电状态。
 */
typedef struct bms_data {
  /**
   * @brief 电池剩余电量
   *
   * 电池的当前电量百分比，范围从 0 到 100，表示电池的剩余电量。
   */
  float battery_percentage;

  /**
   * @brief 电池健康状态
   *
   * 电池的健康状况，通常是一个表示电池性能的浮动值。健康状况越高表示电池越好。
   */
  float battery_health;

  /**
   * @brief 电池状态
   *
   * 电池当前的状态，通常会与 `BatteryState` 枚举类型的值相关联，用来表示电池的不同状态。
   */
  BatteryState battery_state;

  /**
   * @brief 充电状态
   *
   * 一个布尔值，指示电池是否正在充电。`true` 表示电池正在充电，`false` 表示电池未充电。
   */
  PowerSupplyStatus power_supply_status;
} BmsData;

typedef struct robot_state {
  std::vector<Fault> faults;  ///< 故障信息列表
  BmsData bms_data;           ///< 电池管理系统数据
} RobotState;

/************************************************************
 *                        运动控制                           *
 ************************************************************/

/**
 * @brief 运动控制器的层级类型，用于区分不同的控制器职责。
 */
enum class ControllerLevel : int8_t {
  UNKKOWN = 0,
  HighLevel = 1,  ///< 高层级控制器
  LowLevel = 2    ///< 低层级控制器
};

/**
 * @brief 高层运动控制摇杆指令的数据结构
 */
struct JoystickCommand {
  /**
   * @brief 左侧摇杆的X轴方向值
   *
   * 该值表示左侧摇杆沿X轴方向的输入，范围从 -1.0 到 1.0。
   * -1.0 表示左移，1.0 表示右移，0 表示中立位置。
   */
  float left_x_axis;

  /**
   * @brief 左侧摇杆的Y轴方向值
   *
   * 该值表示左侧摇杆沿Y轴方向的输入，范围从 -1.0 到 1.0。
   * -1.0 表示下移，1.0 表示上移，0 表示中立位置。
   */
  float left_y_axis;

  /**
   * @brief 右侧摇杆的X轴方向值
   *
   * 该值表示右侧摇杆沿Z轴方向的旋转，范围从 -1.0 到 1.0。
   * -1.0 表示左旋转，1.0 表示右旋转，0 表示中立位置。
   */
  float right_x_axis;

  /**
   * @brief 右侧摇杆的Y轴方向值，待定
   */
  float right_y_axis;
};
/**
 * @brief 机器人状态枚举，适用于状态机控制
 */
enum class GaitMode : int32_t {
  GAIT_PASSIVE = 0,            // 空闲模式
  GAIT_RECOVERY_STAND = 1,     // 站立锁定/站立恢复
  GAIT_CLASSIC_WALK = 9,       // 经典行走
  GAIT_PURE_DAMPER = 10,       // 阻尼模式
  GAIT_HUMANOID_WALK = 11,     // 拟人行走
  GAIT_ALL_TERRAIN_WALK = 16,  // 全地形行走
  GAIT_FAST_WALK = 17,         // 高速行走
  GAIT_BALANCE_STAND = 46,     // 平衡站立（支持移动）
  GAIT_LOWLEVL_SDK = 200,      // 底层控制SDK模式
};

/**
 * @brief 人形机器人动作指令枚举（对应动作ID）
 */
enum class TrickAction : int32_t {
  ACTION_NONE = 0,                      //无特技, 默认
  ACTION_RECOVERY_STAND = 103,          // 恢复站立
  ACTION_CELEBRATE = 201,               // 庆祝
  ACTION_SHAKE_HAND_REACHOUT = 217,     // 握手 - 伸出
  ACTION_SHAKE_WITH_DRAW = 218,         // 握手 - 撤回
  ACTION_NOD = 219,                     // 点头
  ACTION_SHAKE = 220,                   // 摇头
  ACTION_CIRCLE_HEAD = 221,             // 摇头晃脑
  ACTION_GTEETING = 301,                // 打招呼
  ACTION_POINT_GROUND = 302,            // 指地 -  伸出
  ACTION_POINT_GROUND_WITH_DRAW = 303,  // 指定 - 撤回
  ACTION_SPREAD_HAND = 304,             // 张手 - 伸出
  ACTION_SPREAD_HAND_WITH_DRAW = 305,   // 张手 - 撤回
  ACTION_TURN_AWAY = 306,               // 扭身朝后
  ACTION_TURN_BACK = 307,               // 扭身朝前
};

/**
 * @brief 单个手部关节的控制命令
 */
struct SingleHandJointCommand {
  int16_t operation_mode = 0;  ///< 控制模式（如位置、力矩、阻抗等）
  std::vector<float> pos;      ///< 期望位置数组（7个自由度）
};

/**
 * @brief 整个手部控制命令
 */
struct HandCommand {
  int64_t timestamp;                        ///< 时间戳（单位：纳秒）
  std::vector<SingleHandJointCommand> cmd;  ///< 控制命令数组，依次为左手和右手
};

/**
 * @brief 单个手部关节的状态
 */
struct SingleHandJointState {
  int16_t status_word;     ///< 状态
  std::vector<float> pos;  ///< 实际位置（单位视控制器定义）
  std::vector<float> toq;  ///< 实际力矩（单位：Nm）
  std::vector<float> cur;  ///< 实际电流（单位：A）
  int16_t error_code;      ///< 错误码（0 表示正常）
};

/**
 * @brief 整个手部状态信息
 */
struct HandState {
  int64_t timestamp;                        ///< 时间戳（单位：纳秒）
  std::vector<SingleHandJointState> state;  ///< 所有手部关节状态（共两个），依次为左手和右手
};

/**
 * @brief 单个关节的控制命令
 */
struct SingleJointCommand {
  int16_t operation_mode = 200;  ///< 工作模式（如位置控制、速度控制、力矩控制等）
  float pos;                     ///< 目标位置（单位：rad 或 m，取决于关节类型）
  float vel;                     ///< 目标速度（单位：rad/s 或 m/s）
  float toq;                     ///< 目标力矩（单位：Nm）
  float kp;                      ///< 位置环控制增益（比例项）
  float kd;                      ///< 速度环控制增益（微分项）
};

/**
 * @brief 所有关节控制命令
 *
 * 下肢包含 12 个关节状态项，顺序同控制命令。
 * 上肢包含 14 个关节状态项，顺序同控制命令。
 * 头部包含 2 个关节状态项，顺序同控制命令。
 * 腰部包含 3 个关节状态项，顺序同控制命令。
 */
struct JointCommand {
  int64_t timestamp;                       ///< 时间戳（单位：纳秒）
  std::vector<SingleJointCommand> joints;  ///< 所有关节的控制命令
};

/**
 * @brief 单个关节的状态信息
 */
struct SingleJointState {
  int16_t status_word;  ///< 当前关节状态（自定义状态机编码）
  float posH;           ///< 实际位置（高编码器读取，可能为冗余编码器）
  float posL;           ///< 实际位置（低编码器读取）
  float vel;            ///< 当前速度（单位：rad/s 或 m/s）
  float toq;            ///< 当前力矩（单位：Nm）
  float current;        ///< 当前电流（单位：A）
  int16_t err_code;     ///< 错误码（如编码器异常、电机过流等）
};

/**
 * @brief 所有关节状态数据
 *
 * 下肢包含 12 个关节状态项，顺序同控制命令。
 * 上肢包含 14 个关节状态项，顺序同控制命令。
 * 头部包含 2 个关节状态项，顺序同控制命令。
 * 腰部包含 3 个关节状态项，顺序同控制命令。
 */
struct JointState {
  int64_t timestamp;                     ///< 时间戳（单位：纳秒）
  std::vector<SingleJointState> joints;  ///< 所有关节的状态数据
};

/************************************************************
 *                        语音控制                           *
 ************************************************************/

/**
 * @brief TTS 播报优先级等级
 *
 * 用于控制不同TTS任务之间的中断行为。优先级越高的任务将中断当前低优先级任务的播放。
 */
enum class TtsPriority : int8_t {
  HIGH = 0,    ///< 最高优先级，例如：低电告警、紧急提醒
  MIDDLE = 1,  ///< 中优先级，例如：系统提示、状态播报
  LOW = 2      ///< 最低优先级，例如：日常语音对话、背景播报
};

/**
 * @brief 同一优先级下的任务调度策略
 *
 * 用于细化控制在相同优先级条件下多个TTS任务的播放顺序和清除逻辑。
 */
enum class TtsMode : int8_t {
  CLEARTOP = 0,    ///< 清空当前优先级所有任务（包括正在播放和等待队列），立即播放本次请求
  ADD = 1,         ///< 将本次请求追加到当前优先级队列尾部，顺序播放（不打断当前播放）
  CLEARBUFFER = 2  ///< 清空队列中未播放的请求，保留当前播放，之后播放本次请求
};

/**
 * @brief TTS（Text-To-Speech）播放命令结构体
 *
 * 用于描述一次TTS播放请求的完整信息，支持设置唯一标识、文本内容、优先级控制以及相同优先级下的调度模式。
 *
 * 场景举例：播放天气播报、电量提醒等语音内容时，根据优先级和模式决定播报顺序和中断行为。
 */
typedef struct tts_cmd {
  /**
   * @brief TTS任务唯一ID
   *
   * 用于标识一次TTS任务，在后续回调中追踪TTS状态（如开始播放、播放完成等）。
   * 例如："id_01"
   */
  std::string id;
  /**
   * @brief 要播放的文本内容
   *
   * 支持任意可朗读的UTF-8字符串，例如："你好，欢迎使用智能语音系统。"
   */
  std::string content;
  /**
   * @brief 播报优先级
   *
   * 控制不同TTS请求之间的中断关系，优先级越高的请求会打断正在播放的低优先级请求。
   */
  TtsPriority priority;
  /**
   * @brief 同优先级下的调度模式
   *
   * 控制在相同优先级情况下多个TTS请求的处理逻辑，避免无限扩展优先级值。
   */
  TtsMode mode;
} TtsCommand;

/************************************************************
 *                         传感器                            *
 ************************************************************/

/**
 * @brief IMU 数据结构体，包含时间戳、姿态、角速度、加速度和温度信息
 */
struct Imu {
  int64_t timestamp;              ///< 时间戳（单位：纳秒），表示该IMU数据采集的时间点
  double orientation[4];          ///< 姿态四元数（w, x, y, z），用于表示空间姿态，避免欧拉角万向锁问题
  double angular_velocity[3];     ///< 角速度（单位：rad/s），绕X、Y、Z轴的角速度，通常来自陀螺仪
  double linear_acceleration[3];  ///< 线加速度（单位：m/s^2），X、Y、Z轴的线性加速度，通常来自加速度计
  float temperature;              ///< 温度（单位：摄氏度或其他，应在使用时明确）
};

/**
 * @brief Header结构，包含时间戳与帧名
 */
struct Header {
  int64_t stamp;         ///< 时间戳，单位：纳秒
  std::string frame_id;  ///< 坐标系名称
};

/**
 * @brief 点云字段描述结构体，对应于ROS2中的sensor_msgs::msg::PointField。
 */
struct PointField {
  std::string name;  ///< 字段名，例如"x"、"y"、"z"、"intensity"等
  int32_t offset;    ///< 起始字节偏移
  int8_t datatype;   ///< 数据类型（对应常量）
  int32_t count;     ///< 该字段包含的元素数量
};

/**
 * @brief 通用点云数据结构，类似于 ROS2 的 sensor_msgs::msg::PointCloud2
 */
struct PointCloud2 {
  Header header;  ///< 标准消息头

  int32_t height;  ///< 行数
  int32_t width;   ///< 列数

  std::vector<PointField> fields;  ///< 点字段数组

  bool is_bigendian;   ///< 字节序
  int32_t point_step;  ///< 每个点占用的字节数
  int32_t row_step;    ///< 每行占用的字节数

  std::vector<uint8_t> data;  ///< 原始点云数据（按字段打包）

  bool is_dense;  ///< 是否为稠密点云（无无效点）
};

/**
 * @brief 图像数据结构，支持多种编码格式
 */
struct Image {
  Header header;

  int32_t height;  ///< 图像高度（像素）
  int32_t width;   ///< 图像宽度（像素）

  std::string encoding;  ///< 图像编码类型，如 "rgb8", "mono8", "bgr8"
  bool is_bigendian;     ///< 数据是否为大端模式
  int32_t step;          ///< 每行图像占用的字节数

  std::vector<uint8_t> data;  ///< 原始图像字节数据
};

/**
 * @brief 相机内参与畸变信息，通常与 Image 消息一起发布
 */
struct CameraInfo {
  Header header;

  int32_t height;  ///< 图像高度（行数）
  int32_t width;   ///< 图像宽度（列数）

  std::string distortion_model;  ///< 畸变模型，例如 "plumb_bob"

  std::vector<double> D;  ///< 畸变参数数组

  double K[9];   ///< 相机内参矩阵
  double R[9];   ///< 矫正矩阵
  double P[12];  ///< 投影矩阵

  int32_t binning_x;  ///< 水平binning系数
  int32_t binning_y;  ///< 垂直binning系数

  int32_t roi_x_offset;  ///< ROI起始x
  int32_t roi_y_offset;  ///< ROI起始y
  int32_t roi_height;    ///< ROI高度
  int32_t roi_width;     ///< ROI宽度
  bool roi_do_rectify;   ///< 是否进行矫正
};

/**
 * @brief 三目相机帧数据结构，包含采集/解码时间和三个图像帧
 */
struct TrinocularCameraFrame {
  Header header;  ///< 通用消息头（时间戳+frame_id）

  int64_t vin_time;     ///< 图像采集时间戳，单位：纳秒
  int64_t decode_time;  ///< 图像解码完成时间戳，单位：纳秒

  std::vector<uint8_t> imgfl_array;  ///< 左目图像数据
  std::vector<uint8_t> imgf_array;   ///< 中目图像数据
  std::vector<uint8_t> imgfr_array;  ///< 右目图像数据
};

class NonCopyable {
 protected:
  NonCopyable() = default;
  ~NonCopyable() = default;
  NonCopyable(NonCopyable&&) = default;
  NonCopyable& operator=(NonCopyable&&) = default;
  NonCopyable(const NonCopyable&) = delete;
  NonCopyable& operator=(const NonCopyable&) = delete;
};

}  // namespace magic::robot
