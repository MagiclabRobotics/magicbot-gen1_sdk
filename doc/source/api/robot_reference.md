# 机器人主控服务

> 提供机器人系统主控制器，通过MagicRobot可以进行资源初始化、管理通信连接、访问各子控制器如运动控制器、音频、状态监控以及传感器控制器等。

## 接口定义
`MagicRobot` 是机器人系统的统一入口类。

### MagicRobot
| 项目 | 内容 |
|------|------|
| 函数名 | MagicRobot |
| 函数声明 | `MagicRobot();` |
| 功能概述 | 构造函数，创建 MagicRobot 实例。 |
| 备注 | 构造内部状态。 |

### ~MagicRobot
| 项目 | 内容 |
|------|------|
| 函数名 | ~MagicRobot |
| 函数声明 | `~MagicRobot();` |
| 功能概述 | 析构函数，释放 MagicRobot 实例资源。 |
| 备注 | 确保资源安全释放。 |

### Initialize
| 项目 | 内容 |
|------|------|
| 函数名 | Initialize |
| 函数声明 | `bool Initialize(const std::string& local_ip);` |
| 功能概述 | 初始化机器人系统，包括控制器与网络模块。 |
| 参数说明 | `local_ip`：本地通信IP地址。 |
| 返回值 | `true` 表示成功，`false` 表示失败。 |
| 备注 | 首次使用前必须调用。 |

### Shutdown
| 项目 | 内容 |
|------|------|
| 函数名 | Shutdown |
| 函数声明 | `void Shutdown();` |
| 功能概述 | 关闭机器人系统，释放资源。 |
| 备注 | 配合 Initialize 使用。 |

### Connect
| 项目 | 内容 |
|------|------|
| 函数名 | Connect |
| 函数声明 | `Status Connect();` |
| 功能概述 | 与机器人服务建立通信连接。 |
| 返回值 | `Status::OK` 表示成功。 |
| 备注 | 阻塞接口，需初始化后调用。 |

### Disconnect
| 项目 | 内容 |
|------|------|
| 函数名 | Disconnect |
| 函数声明 | `Status Disconnect();` |
| 功能概述 | 断开与机器人服务的连接。 |
| 返回值 | gRPC 调用状态。 |
| 备注 | 阻塞接口，与 Connect 配对使用。 |

### GetSDKVersion
| 项目 | 内容 |
|------|------|
| 函数名 | GetSDKVersion |
| 函数声明 | `std::string GetSDKVersion() const;` |
| 功能概述 | 获取当前 SDK 的版本号。 |
| 返回值 | SDK 版本字符串（如 `0.0.1`）。 |
| 备注 | 非阻塞接口，便于调试或日志标记。 |

### SetTimeout
| 项目 | 内容 |
|------|------|
| 函数名 | SetTimeout |
| 函数声明 | `void SetTimeout(int timeout);` |
| 功能概述 | 设置接口调用的超时时间。 |
| 参数说明 | `timeout`：单位为毫秒。 |
| 返回值 | 无 |
| 备注 | 非阻塞接口，默认值为 5000 毫秒。 |

### GetMotionControlLevel
| 项目 | 内容 |
|------|------|
| 函数名 | GetMotionControlLevel |
| 函数声明 | `ControllerLevel GetMotionControlLevel();` |
| 功能概述 | 获取当前运动控制级别（高层/低层）。 |
| 返回值 | `ControllerLevel` 枚举值。 |
| 备注 | 非阻塞接口，用于判断当前控制权限。 |

### SetMotionControlLevel
| 项目 | 内容 |
|------|------|
| 函数名 | SetMotionControlLevel |
| 函数声明 | `Status SetMotionControlLevel(ControllerLevel level);` |
| 功能概述 | 设置当前运动控制级别。 |
| 参数说明 | `level`：控制权限枚举值。 |
| 返回值 | `Status::OK` 表示设置成功，其他代表设置失败。 |
| 备注 | 阻塞接口，控制模式切换时使用。 |

### GetHighLevelMotionController
| 项目 | 内容 |
|------|------|
| 函数名 | GetHighLevelMotionController |
| 函数声明 | `HighLevelMotionController& GetHighLevelMotionController();` |
| 功能概述 | 获取高层运动控制器对象。 |
| 返回值 | 引用类型，用于调用高层控制接口。 |
| 备注 | 非阻塞接口，封装了步态、特技、遥控等控制。 |

### GetLowLevelMotionController
| 项目 | 内容 |
|------|------|
| 函数名 | GetLowLevelMotionController |
| 函数声明 | `LowLevelMotionController& GetLowLevelMotionController();` |
| 功能概述 | 获取低层运动控制器对象。 |
| 返回值 | 引用类型，用于控制关节或电机。 |
| 备注 | 非阻塞接口，直接控制关节电机、获取imu等。 |

### GetAudioController
| 项目 | 内容 |
|------|------|
| 函数名 | GetAudioController |
| 函数声明 | `AudioController& GetAudioController();` |
| 功能概述 | 获取音频控制器对象。 |
| 返回值 | 引用类型，用于语音控制。 |
| 备注 | 非阻塞接口，播放语音和控制音量。 |

### GetSensorController
| 项目 | 内容 |
|------|------|
| 函数名 | GetSensorController |
| 函数声明 | `SensorController& GetSensorController();` |
| 功能概述 | 获取传感器控制器对象。 |
| 返回值 | 引用类型，用于访问传感器数据。 |
| 备注 | 非阻塞接口，封装了 IMU、RGBD 等读取。 |


### GetStateMonitor
| 项目 | 内容 |
|------|------|
| 函数名 | GetStateMonitor |
| 函数声明 | `StateMonitor& GetStateMonitor();` |
| 功能概述 | 获取状态监控器对象。 |
| 返回值 | 引用类型，，用于获取机器人当前状态信息。 |
| 备注 | 非阻塞接口，封装了 BMS、故障 等状态信息的读取。 |


