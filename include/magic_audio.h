#pragma once

#include "magic_export.h"
#include "magic_type.h"

#include <atomic>
#include <functional>
#include <memory>
#include <string>

namespace magic::gen1::audio {

class AudioController;
using AudioControllerPtr = std::unique_ptr<AudioController>;

/**
 * @class AudioController
 * @brief 封装音频控制功能的类，提供音频播放、停止、音量调节等接口。
 *
 * 该类通常用于控制机器人或智能设备中的音频输出，支持文本转语音（TTS）播放、
 * 音量设置与查询，并提供初始化和资源释放机制。
 */
class MAGIC_EXPORT_API AudioController final : public NonCopyable {
  // 消息指针类型定义（智能指针，便于内存管理）
  using AudioStreamPtr = std::shared_ptr<AudioStream>;  // IMU 惯性测量单元消息指针
  // 音频流数据的回调函数类型定义
  using OriginAudioStreamCallback = std::function<void(const AudioStreamPtr)>;  // Origin音频流数据的回调
  using BfAudioStreamCallback = std::function<void(const AudioStreamPtr)>;      // Origin音频流数据的回调

 public:
  /**
   * @brief 构造函数，初始化音频控制器对象。
   *        可用于构造内部状态，分配资源等。
   */
  AudioController();

  /**
   * @brief 析构函数，释放音频控制器资源。
   *        确保停止播放并清理底层资源。
   */
  ~AudioController();

  /**
   * @brief 初始化音频控制模块。
   * @return 成功返回 true，失败返回 false。
   */
  bool Initialize();

  /**
   * @brief 关闭音频控制器并释放资源。
   *        与 Initialize 配套使用，确保安全退出。
   */
  void Shutdown();

  /**
   * @brief 播放语音命令（TTS）。
   * @param cmd TTS命令，包含文本内容、语速、语调等参数。
   * @return 操作状态，成功返回 Status::OK。
   */
  Status Play(const TtsCommand& cmd);

  /**
   * @brief 停止当前音频播放。
   * @return 操作状态，成功返回 Status::OK。
   */
  Status Stop();

  /**
   * @brief 设置音频输出的音量。
   * @param volume 音量值（通常范围 0-100 或协议定义的范围）。
   * @return 操作状态，成功返回 Status::OK。
   */
  Status SetVolume(int volume);

  /**
   * @brief 获取当前音频输出音量。
   * @param[out] volume 当前音量值（通过引用返回）。
   * @return 操作状态，成功返回 Status::OK。
   */
  Status GetVolume(int& volume);

  /**
   * @brief 打开音频流，准备进行音频播放。
   * @return 操作状态，成功返回 Status::OK。
   */
  Status OpenAudioStream();

  /**
   * @brief 关闭音频流。
   * @return 操作状态，成功返回 Status::OK。
   */
  Status CloseAudioStream();

  /**
   * @brief 订阅原始音频流数据
   * @param callback 接收到原始音频流数据后的处理回调
   */
  void SubscribeOriginAudioStream(const OriginAudioStreamCallback callback);

  /**
   * @brief 订阅 BF 音频流数据
   * @param callback 接收到 BF 音频流数据后的处理回调
   */
  void SubscribeBfAudioStream(const BfAudioStreamCallback callback);

 private:
  std::atomic_bool is_shutdown_{true};  // 标记是否已初始化
};

}  // namespace magic::gen1::audio