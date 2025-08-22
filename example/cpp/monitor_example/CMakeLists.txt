add_executable(monitor_example monitor_example.cpp)

target_link_libraries(
  monitor_example
  PRIVATE magicbot_gen1::sdk)
