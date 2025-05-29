
# 状态监控服务

> 提供机器人状态监控接口类，通过StateMonitor可以提供状态查询等接口。

## 接口定义
`StateMonitor` 是机器人系统状态监控管理类，该类通常用于控制机器人的状态管理，支持状态查询。

### GetCurrentState
| 项目 | 内容 |
|------|------|
| 函数名 | GetCurrentState |
| 函数声明 | `RobotState GetCurrentState();` |
| 功能概述 | 获取当前机器人聚合状态。 |
| 参数说明 | `robot_state`：用于接收状态结构体。 |
| 返回值 | `RobotState` 对象。 |
| 备注 | 非阻塞接口，获取最近监控到的机器人状态数据，包括BMS/故障状态监控等，后续会迭代拓展。 |

### `RobotState` — 机器人状态数据结构体

用于表示机器人总体状态信息：

| 字段名     | 类型                | 描述           |
|------------|---------------------|----------------|
| `faults`   | `std::vector<Fault>`| 故障信息列表   |
| `bms_data` | `BmsData`           | 电池管理系统数据 |


### `BmsData` — 电池管理系统数据结构体

表示电池的状态信息：

| 字段名                  | 类型                 | 描述                                     |
|------------------------|----------------------|------------------------------------------|
| `battery_percentage`   | `float`              | 当前电池剩余电量（百分比，0~100）        |
| `battery_health`       | `float`              | 电池健康状态（越高越好）                 |
| `battery_state`        | `BatteryState`       | 电池状态（见上方枚举）                   |
| `power_supply_status`  | `PowerSupplyStatus`  | 电池充放电状态（见上方枚举）             |



### 枚举类型定义

#### `BatteryState` — 电池状态枚举类型

用于表示电池当前的状态，用于系统中电池状态的判断和处理：

| 枚举值                          | 数值 | 描述               |
|--------------------------------|------|--------------------|
| `BatteryState::UNKNOWN`        | 0    | 未知状态           |
| `BatteryState::GOOD`           | 1    | 电池状态良好       |
| `BatteryState::OVERHEAT`       | 2    | 电池过热           |
| `BatteryState::DEAD`           | 3    | 电池损坏           |
| `BatteryState::OVERVOLTAGE`    | 4    | 电池过电压         |
| `BatteryState::UNSPEC_FAILURE` | 5    | 未知故障           |
| `BatteryState::COLD`           | 6    | 电池过冷           |
| `BatteryState::WATCHDOG_TIMER_EXPIRE` | 7 | 看门狗定时器超时 |
| `BatteryState::SAFETY_TIMER_EXPIRE`   | 8 | 安全定时器超时   |


#### `PowerSupplyStatus` — 电池充放电状态

用于表示当前电池的充放电状态：

| 枚举值                          | 数值 | 描述           |
|--------------------------------|------|----------------|
| `PowerSupplyStatus::UNKNOWN`     | 0    | 未知状态       |
| `PowerSupplyStatus::CHARGING`    | 1    | 电池充电中     |
| `PowerSupplyStatus::DISCHARGING` | 2    | 电池放电中     |
| `PowerSupplyStatus::NOTCHARGING` | 3    | 电池未充放电   |
| `PowerSupplyStatus::FULL`        | 4    | 电池充满       |




## 错误码映射表

| 错误码（十六进制） | 错误描述                              |
|-------------------|--------------------------------------|
| 0x0000            | No fault                             |
| 0x1101            | Service invocation failed            |
| 0x1301            | Central control node lost            |
| 0x1302            | App node lost                        |
| 0x1303            | Audio node lost                      |
| 0x1304            | Stereo camera node lost              |
| 0x1305            | LIDAR node lost                      |
| 0x1306            | SLAM node lost                       |
| 0x1307            | Navigation node lost                 |
| 0x1308            | AI node lost                         |
| 0x1309            | Head node lost                       |
| 0x130A            | Point cloud node lost                |
| 0x2201            | No LIDAR data received               |
| 0x2202            | No stereo camera data received       |
| 0x2203            | Stereo camera data error             |
| 0x2204            | Stereo camera initialization failed  |
| 0x220B            | No odometry data received            |
| 0x220C            | No IMU data received                 |
| 0x2215            | Depth camera not detected            |
| 0x3101            | Failed to connect robot to app       |
| 0x3102            | Heartbeat lost - assertion failed    |
| 0x4201            | Failed to open head serial port      |
| 0x4202            | No head data received                |
| 0x5201            | No navigation TF data                |
| 0x5202            | No navigation map data               |
| 0x5203            | No navigation localization data      |
| 0x5204            | No navigation LIDAR data             |
| 0x5205            | No navigation depth camera data      |
| 0x5206            | No navigation multi-line LIDAR data  |
| 0x5207            | No navigation odometry data          |
| 0x6201            | SLAM localization error              |
| 0x6102            | No SLAM LIDAR data                   |
| 0x6103            | No SLAM odometry data                |
| 0x6104            | SLAM map data error                  |
| 0x7201            | LCM connection timeout               |
| 0x8201            | Left leg hardware error              |
| 0x8202            | Right leg hardware error             |
| 0x8203            | Left arm hardware error              |
| 0x8204            | Right arm hardware error             |
| 0x8205            | Waist hardware error                 |
| 0x8206            | Head hardware error                  |
| 0x8207            | Hand hardware error                  |
| 0x8208            | Gripper hardware error               |
| 0x8209            | IMU hardware error                   |
| 0x820A            | Power system hardware error          |
| 0x820B            | Leg force sensor hardware error      |
| 0x820C            | Arm force sensor hardware error      |
| 0x9201            | ECAT (EtherCAT) hardware error       |
| 0xA201            | Motion posture error                 |
| 0xA202            | Foot position deviation during movement |
| 0xA203            | Joint velocity error during motion   |
