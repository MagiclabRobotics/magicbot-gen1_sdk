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
 * @brief Class that encapsulates audio control functionality, providing interfaces for audio playback, stopping, volume adjustment, etc.
 *
 * This class is typically used to control audio output in robots or smart devices, supporting text-to-speech (TTS) playback,
 * volume setting and querying, and providing initialization and resource release mechanisms.
 */
class MAGIC_EXPORT_API AudioController final : public NonCopyable {
  // Message pointer type definitions (smart pointers for memory management)
  using AudioStreamPtr = std::shared_ptr<AudioStream>;  // Audio stream message pointer
  // Audio stream data callback function type definitions
  using OriginAudioStreamCallback = std::function<void(const AudioStreamPtr)>;  // Origin audio stream data callback
  using BfAudioStreamCallback = std::function<void(const AudioStreamPtr)>;      // BF audio stream data callback

 public:
  /**
   * @brief Constructor, initializes audio controller object.
   *        Can be used to construct internal state, allocate resources, etc.
   */
  AudioController();

  /**
   * @brief Destructor, releases audio controller resources.
   *        Ensures playback stops and cleans up underlying resources.
   */
  ~AudioController();

  /**
   * @brief Initialize audio control module.
   * @return Returns true on success, false on failure.
   */
  bool Initialize();

  /**
   * @brief Close audio controller and release resources.
   *        Used together with Initialize to ensure safe exit.
   */
  void Shutdown();

  /**
   * @brief Play voice command (TTS).
   * @param cmd TTS command containing text content, speed, tone and other parameters.
   * @param timeout_ms Timeout in milliseconds.
   * @return Operation status, returns Status::OK on success.
   */
  Status Play(const TtsCommand& cmd, int timeout_ms = 5000);

  /**
   * @brief Stop current audio playback.
   * @return Operation status, returns Status::OK on success.
   */
  Status Stop();

  /**
   * @brief Set audio output volume.
   * @param volume Volume value (typically range 0-100 or protocol-defined range).
   * @return Operation status, returns Status::OK on success.
   */
  Status SetVolume(int volume);

  /**
   * @brief Get current audio output volume.
   * @param[out] volume Current volume value (returned by reference).
   * @return Operation status, returns Status::OK on success.
   */
  Status GetVolume(int& volume);

  /**
   * @brief Open audio stream, prepare for audio playback.
   * @return Operation status, returns Status::OK on success.
   */
  Status OpenAudioStream();

  /**
   * @brief Close audio stream.
   * @return Operation status, returns Status::OK on success.
   */
  Status CloseAudioStream();

  /**
   * @brief Subscribe to original audio stream data
   * @param callback Processing callback after receiving original audio stream data
   */
  void SubscribeOriginAudioStream(const OriginAudioStreamCallback callback);

  /**
   * @brief Subscribe to BF audio stream data
   * @param callback Processing callback after receiving BF audio stream data
   */
  void SubscribeBfAudioStream(const BfAudioStreamCallback callback);

 private:
  std::atomic_bool is_shutdown_{true};  // Flag indicating whether initialized
};

}  // namespace magic::gen1::audio