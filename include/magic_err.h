#pragma once

#include <cstdint>
#include <string>
#include <unordered_map>
namespace magic::gen1 {

static std::unordered_map<uint16_t, std::string> error_code_map = {
    {0x0000, "No fault"},

    {0x1101, "Service invocation failed"},
    {0x1301, "Central control node lost"},
    {0x1302, "App node lost"},
    {0x1303, "Audio node lost"},
    {0x1304, "Stereo camera node lost"},
    {0x1305, "LIDAR node lost"},
    {0x1306, "SLAM node lost"},
    {0x1307, "Navigation node lost"},
    {0x1308, "AI node lost"},
    {0x1309, "Head node lost"},
    {0x130A, "Point cloud node lost"},

    {0x2201, "No LIDAR data received"},
    {0x2202, "No stereo camera data received"},
    {0x2203, "Stereo camera data error"},
    {0x2204, "Stereo camera initialization failed"},
    {0x220B, "No odometry data received"},
    {0x220C, "No IMU data received"},
    {0x2215, "Depth camera not detected"},

    {0x3101, "Failed to connect robot to app"},
    {0x3102, "Heartbeat lost - assertion failed"},

    {0x4201, "Failed to open head serial port"},
    {0x4202, "No head data received"},

    {0x5201, "No navigation TF data"},
    {0x5202, "No navigation map data"},
    {0x5203, "No navigation localization data"},
    {0x5204, "No navigation LIDAR data"},
    {0x5205, "No navigation depth camera data"},
    {0x5206, "No navigation multi-line LIDAR data"},
    {0x5207, "No navigation odometry data"},

    {0x6201, "SLAM localization error"},
    {0x6102, "No SLAM LIDAR data"},
    {0x6103, "No SLAM odometry data"},
    {0x6104, "SLAM map data error"},

    {0x7201, "LCM connection timeout"},

    {0x8201, "Left leg hardware error"},
    {0x8202, "Right leg hardware error"},
    {0x8203, "Left arm hardware error"},
    {0x8204, "Right arm hardware error"},
    {0x8205, "Waist hardware error"},
    {0x8206, "Head hardware error"},
    {0x8207, "Hand hardware error"},
    {0x8208, "Gripper hardware error"},
    {0x8209, "IMU hardware error"},
    {0x820A, "Power system hardware error"},
    {0x820B, "Leg force sensor hardware error"},
    {0x820C, "Arm force sensor hardware error"},

    {0x9201, "ECAT (EtherCAT) hardware error"},

    {0xA201, "Motion posture error"},
    {0xA202, "Foot position deviation during movement"},
    {0xA203, "Joint velocity error during motion"}};

}