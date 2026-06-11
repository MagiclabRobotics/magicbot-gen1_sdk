add_executable(hybrid_motion_example hybrid_motion_example.cpp)

target_link_libraries(
  hybrid_motion_example
  PRIVATE magicbot_gen1::sdk)
