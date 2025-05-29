# 传感器服务

> 提供机器人系统传感器（雷达/rgbd相机/三目相机）服务，通过SensorController可以通过RPC和话题方式实现对机器人的传感器进行指令控制和状态获取。


## 接口定义
`SensorController` 是封装机器人各类传感器管理的 C++ 类，支持 IMU、点云、RGBD 相机与三目相机的初始化、控制与数据订阅。

> ⚠️ **Notice:** 当前Lidar/RGBD/三目相机传感器接口暂未完全开放。


### SensorController
| 项目 | 内容 |
|------|------|
| 函数名 | SensorController |
| 函数声明 | `SensorController();` |
| 功能概述 | 构造函数，初始化传感器控制器对象。 |
| 备注 | 构造内部状态。 |

### ~SensorController
| 项目 | 内容 |
|------|------|
| 函数名 | ~SensorController |
| 函数声明 | `virtual ~SensorController();` |
| 功能概述 | 析构函数，释放所有传感器资源。 |
| 备注 | 调用前应关闭传感器。 |

### Initialize
| 项目 | 内容 |
|------|------|
| 函数名 | Initialize |
| 函数声明 | `bool Initialize();` |
| 功能概述 | 初始化控制器，包括资源申请和驱动加载。 |
| 返回值 | `true` 表示成功，`false` 表示失败。 |
| 备注 | 调用前需先构造对象。 |

### Shutdown
| 项目 | 内容 |
|------|------|
| 函数名 | Shutdown |
| 函数声明 | `void Shutdown();` |
| 功能概述 | 关闭所有传感器连接并释放资源。 |
| 备注 | 配合 Initialize 使用。 |

### OpenLidar
| 项目 | 内容 |
|------|------|
| 函数名 | OpenLidar |
| 函数声明 | `Status OpenLidar();` |
| 功能概述 | 打开雷达。 |
| 返回值 | `Status::OK` 表示成功，其他为失败。 |
| 备注 | 阻塞接口。 |

### CloseLidar
| 项目 | 内容 |
|------|------|
| 函数名 | CloseLidar |
| 函数声明 | `Status CloseLidar();` |
| 功能概述 | 关闭 雷达。 |
| 返回值 | `Status::OK` 表示成功，其他为失败。 |
| 备注 | 阻塞接口，配合打开函数使用。 |

### OpenRgbdCamera
| 项目 | 内容 |
|------|------|
| 函数名 | OpenRgbdCamera |
| 函数声明 | `Status OpenRgbdCamera();` |
| 功能概述 | 打开 RGBD 相机（头部与腰部）。 |
| 返回值 | `Status::OK` 表示成功，其他为失败。 |
| 备注 | 阻塞接口。 |

### CloseRgbdCamera
| 项目 | 内容 |
|------|------|
| 函数名 | CloseRgbdCamera |
| 函数声明 | `Status CloseRgbdCamera();` |
| 功能概述 | 关闭 RGBD 相机。 |
| 返回值 | `Status::OK` 表示成功，其他为失败。 |
| 备注 | 阻塞接口，配合打开函数使用。 |

### OpenTrinocularCamera
| 项目 | 内容 |
|------|------|
| 函数名 | OpenTrinocularCamera |
| 函数声明 | `Status OpenTrinocularCamera();` |
| 功能概述 | 打开三目相机。 |
| 返回值 | `Status::OK` 表示成功，其他为失败。 |
| 备注 | 阻塞接口。 |

### CloseTrinocularCamera
| 项目 | 内容 |
|------|------|
| 函数名 | CloseTrinocularCamera |
| 函数声明 | `Status CloseTrinocularCamera();` |
| 功能概述 | 关闭三目相机。 |
| 返回值 | `Status::OK` 表示成功，其他为失败。 |
| 备注 | 阻塞接口，。 |

### SubscribeLidarImu
| 项目 | 内容 |
|------|------|
| 函数名 | SubscribeLidarImu |
| 函数声明 | `void SubscribeLidarImu(const LidarImuCallback& callback);` |
| 功能概述 | 订阅雷达 IMU 数据 |
| 参数说明 | callback：接收到数据后的处理函数 |
| 备注 | 非阻塞接口，回调函数会在数据更新时被调用。 |

### SubscribeLidarPointCloud
| 项目 | 内容 |
|------|------|
| 函数名 | SubscribeLidarPointCloud |
| 函数声明 | `void SubscribeLidarPointCloud(const LidarPointCloudCallback& callback);` |
| 功能概述 | 订阅雷达点云数据 |
| 参数说明 | callback：接收到点云后的处理函数 |
| 备注 | 非阻塞接口，回调函数会在数据更新时被调用。 |

### SubscribeHeadRgbdColorImage
| 项目 | 内容 |
|------|------|
| 函数名 | SubscribeHeadRgbdColorImage |
| 函数声明 | `void SubscribeHeadRgbdColorImage(const RgbdImageCallback& callback);` |
| 功能概述 | 订阅头部 RGBD 彩色图像数据 |
| 参数说明 | callback：接收到图像后的处理函数 |
| 备注 | 非阻塞接口，回调函数会在数据更新时被调用。 |

### SubscribeHeadRgbdColorCameraInfo
| 项目 | 内容 |
|------|------|
| 函数名 | SubscribeHeadRgbdColorCameraInfo |
| 函数声明 | `void SubscribeHeadRgbdColorCameraInfo(const RgbdCameraInfoCallback& callback);` |
| 功能概述 | 订阅头部 RGBD 彩色相机参数 |
| 参数说明 | callback：接收到参数后的处理函数 |
| 备注 | 非阻塞接口，回调函数会在数据更新时被调用。 |


### SubscribeHeadRgbdDepthImage
| 项目 | 内容 |
|------|------|
| 函数名 | SubscribeHeadRgbdDepthImage |
| 函数声明 | `void SubscribeHeadRgbdDepthImage(const RgbdImageCallback& callback);` |
| 功能概述 | 订阅头部 RGBD 深度图像数据 |
| 参数说明 | callback：接收到图像后的处理函数 |
| 备注 | 非阻塞接口，回调函数会在数据更新时被调用。 |

### SubscribeHeadRgbdDepthCameraInfo
| 项目 | 内容 |
|------|------|
| 函数名 | SubscribeHeadRgbdDepthCameraInfo |
| 函数声明 | `void SubscribeHeadRgbdDepthCameraInfo(const RgbdCameraInfoCallback& callback);` |
| 功能概述 | 订阅头部 RGBD 深度相机参数 |
| 参数说明 | callback：接收到参数后的处理函数 |
| 备注 | 非阻塞接口，回调函数会在数据更新时被调用。 |

### SubscribeWaistRgbdColorImage
| 项目 | 内容 |
|------|------|
| 函数名 | SubscribeWaistRgbdColorImage |
| 函数声明 | `void SubscribeWaistRgbdColorImage(const RgbdImageCallback& callback);` |
| 功能概述 | 订阅腰部 RGBD 彩色图像数据 |
| 参数说明 | callback：接收到图像后的处理函数 |
| 备注 | 非阻塞接口，回调函数会在数据更新时被调用。 |

### SubscribeWaistRgbdColorCameraInfo
| 项目 | 内容 |
|------|------|
| 函数名 | SubscribeWaistRgbdColorCameraInfo |
| 函数声明 | `void SubscribeWaistRgbdColorCameraInfo(const RgbdCameraInfoCallback& callback);` |
| 功能概述 | 订阅腰部 RGBD 彩色相机参数 |
| 参数说明 | callback：接收到参数后的处理函数 |
| 备注 | 非阻塞接口，回调函数会在数据更新时被调用。 |

### SubscribeWaistRgbdDepthImage
| 项目 | 内容 |
|------|------|
| 函数名 | SubscribeWaistRgbdDepthImage |
| 函数声明 | `void SubscribeWaistRgbdDepthImage(const RgbdImageCallback& callback);` |
| 功能概述 | 订阅腰部 RGBD 深度图像数据 |
| 参数说明 | callback：接收到图像后的处理函数 |
| 备注 | 非阻塞接口，回调函数会在数据更新时被调用。 |

### SubscribeWaistRgbdDepthCameraInfo
| 项目 | 内容 |
|------|------|
| 函数名 | SubscribeWaistRgbdDepthCameraInfo |
| 函数声明 | `void SubscribeWaistRgbdDepthCameraInfo(const RgbdCameraInfoCallback& callback);` |
| 功能概述 | 订阅腰部 RGBD 深度相机参数 |
| 参数说明 | callback：接收到参数后的处理函数 |
| 备注 | 非阻塞接口，回调函数会在数据更新时被调用。 |

### SubscribeTrinocularImage
| 项目 | 内容 |
|------|------|
| 函数名 | SubscribeTrinocularImage |
| 函数声明 | `void SubscribeTrinocularImage(const TrinocularImageCallback& callback);` |
| 功能概述 | 订阅三目相机图像帧 |
| 参数说明 | callback：接收到图像帧后的处理函数 |
| 备注 | 非阻塞接口，回调函数会在数据更新时被调用。 |


## 类型定义

### `Imu` — IMU 数据结构体

| 字段名                 | 类型          | 描述                                                             |
|------------------------|---------------|------------------------------------------------------------------|
| `timestamp`            | `int64_t`     | 时间戳（单位：纳秒）                                             |
| `orientation[4]`       | `double[4]`   | 姿态四元数（w, x, y, z）                                         |
| `angular_velocity[3]`  | `double[3]`   | 角速度（单位：rad/s）                                            |
| `linear_acceleration[3]`| `double[3]`  | 线加速度（单位：m/s²）                                           |
| `temperature`          | `float`       | 温度（单位：摄氏度或其他，应明确单位）                          |

---

### `Header` — 通用消息头结构体

| 字段名     | 类型            | 描述           |
|------------|-----------------|----------------|
| `stamp`    | `int64_t`       | 时间戳（单位：纳秒） |
| `frame_id` | `std::string`   | 坐标系名称     |

---

### `PointField` — 点字段描述

| 字段名    | 类型           | 描述                        |
|-----------|----------------|-----------------------------|
| `name`    | `std::string`  | 字段名（如 x、y、z、intensity） |
| `offset`  | `int32_t`      | 起始字节偏移                |
| `datatype`| `int8_t`       | 数据类型（对应常量）         |
| `count`   | `int32_t`      | 每点此字段包含元素数量       |

---

### `PointCloud2` — 点云数据结构体

| 字段名        | 类型                       | 描述                           |
|---------------|----------------------------|--------------------------------|
| `header`      | `Header`                   | 消息头                         |
| `height`      | `int32_t`                  | 行数                           |
| `width`       | `int32_t`                  | 列数                           |
| `fields`      | `std::vector<PointField>`  | 点字段数组                     |
| `is_bigendian`| `bool`                     | 字节序                         |
| `point_step`  | `int32_t`                  | 每个点的字节数                 |
| `row_step`    | `int32_t`                  | 每行的字节数                   |
| `data`        | `std::vector<uint8_t>`     | 原始点云字节数据               |
| `is_dense`    | `bool`                     | 是否稠密点云（无无效点）       |

---

### `Image` — 图像数据结构体

| 字段名        | 类型                     | 描述                       |
|---------------|--------------------------|----------------------------|
| `header`      | `Header`                 | 消息头                     |
| `height`      | `int32_t`                | 图像高度（像素）           |
| `width`       | `int32_t`                | 图像宽度（像素）           |
| `encoding`    | `std::string`            | 编码类型（如 rgb8, mono8） |
| `is_bigendian`| `bool`                   | 是否为大端模式             |
| `step`        | `int32_t`                | 每行图像占用字节数         |
| `data`        | `std::vector<uint8_t>`   | 原始图像字节数据           |

---

### `CameraInfo` — 相机内参与畸变信息

| 字段名             | 类型                    | 描述                        |
|--------------------|-------------------------|-----------------------------|
| `header`           | `Header`                | 消息头                      |
| `height`           | `int32_t`               | 图像高度                    |
| `width`            | `int32_t`               | 图像宽度                    |
| `distortion_model` | `std::string`           | 畸变模型（如 plumb_bob）    |
| `D`                | `std::vector<double>`   | 畸变参数数组                |
| `K`                | `double[9]`             | 相机内参矩阵                |
| `R`                | `double[9]`             | 矫正矩阵                    |
| `P`                | `double[12]`            | 投影矩阵                    |
| `binning_x`        | `int32_t`               | 水平 binning 系数          |
| `binning_y`        | `int32_t`               | 垂直 binning 系数          |
| `roi_x_offset`     | `int32_t`               | ROI 起始 x 坐标            |
| `roi_y_offset`     | `int32_t`               | ROI 起始 y 坐标            |
| `roi_height`       | `int32_t`               | ROI 高度                   |
| `roi_width`        | `int32_t`               | ROI 宽度                   |
| `roi_do_rectify`   | `bool`                  | 是否进行矫正                |

---

### `TrinocularCameraFrame` — 三目相机帧数据结构

| 字段名        | 类型                     | 描述                         |
|---------------|--------------------------|------------------------------|
| `header`      | `Header`                 | 通用消息头                   |
| `vin_time`    | `int64_t`                | 图像采集时间（纳秒）         |
| `decode_time` | `int64_t`                | 图像解码时间（纳秒）         |
| `imgfl_array` | `std::vector<uint8_t>`   | 左目图像数据                 |
| `imgf_array`  | `std::vector<uint8_t>`   | 中目图像数据                 |
| `imgfr_array` | `std::vector<uint8_t>`   | 右目图像数据                 |
