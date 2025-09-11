#!/usr/bin/env python3

import sys
import time
import signal
import logging
from typing import Optional

import magicbot_gen1_python as magicbot

# Configure logging format and level
logging.basicConfig(
    level=logging.INFO,  # Minimum log level
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# Global variables
robot: Optional[magicbot.MagicRobot] = None


def signal_handler(signum, frame):
    """Signal handler function for graceful exit"""
    global robot
    logging.info(f"Received interrupt signal ({signum}), exiting...")
    if robot:
        robot.disconnect()
        logging.info("Robot disconnected")
        robot.shutdown()
        logging.info("Robot shutdown")
    exit(-1)


imu_counter = 0


def lidar_imu_callback(imu_data):
    """LiDAR IMU data callback function"""
    global imu_counter
    imu_counter += 1
    if imu_counter % 100 == 0:
        logging.info("+++++++++++++ Received LiDAR IMU data")
        logging.info(
            "Received LiDAR IMU data, counter: %d, timestamp: %d",
            imu_counter,
            imu_data.timestamp,
        )
        logging.info("Received LiDAR IMU data, orientation: %s", imu_data.orientation)
        logging.info(
            "Received LiDAR IMU data, angular_velocity: %s", imu_data.angular_velocity
        )
        logging.info(
            "Received LiDAR IMU data, linear_acceleration: %s",
            imu_data.linear_acceleration,
        )
        logging.info("Received LiDAR IMU data, temperature: %s", imu_data.temperature)


point_cloud_counter = 0


def lidar_point_cloud_callback(point_cloud_data):
    """LiDAR point cloud data callback function"""
    global point_cloud_counter
    point_cloud_counter += 1
    logging.info("Received LiDAR point cloud data, counter: %d", point_cloud_counter)


def main():
    """Main function"""
    global robot

    # Bind signal handler
    signal.signal(signal.SIGINT, signal_handler)

    logging.info("Robot model: %s", magicbot.get_robot_model())

    # Create robot instance
    robot = magicbot.MagicRobot()

    try:
        # Configure local IP address for direct network connection and initialize SDK
        local_ip = "192.168.54.111"
        if not robot.initialize(local_ip):
            logging.error("Failed to initialize robot SDK")
            robot.shutdown()
            return -1

        # Set RPC timeout to 20 seconds
        robot.set_timeout(20000)

        # Connect to robot
        status = robot.connect()
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "Failed to connect to robot, code: %s, message: %s",
                status.code,
                status.message,
            )
            robot.shutdown()
            return -1

        logging.info("Successfully connected to robot")

        # Get sensor controller
        controller = robot.get_sensor_controller()

        # Open LiDAR
        status = controller.open_lidar()
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "Failed to open LiDAR, code: %s, message: %s",
                status.code,
                status.message,
            )
            robot.shutdown()
            return -1

        logging.info("LiDAR opened successfully")

        # Subscribe to LiDAR IMU data
        controller.subscribe_lidar_imu(lidar_imu_callback)
        logging.info("Subscribed to LiDAR IMU data")

        # Subscribe to LiDAR point cloud data
        controller.subscribe_lidar_point_cloud(lidar_point_cloud_callback)
        logging.info("Subscribed to LiDAR point cloud data")

        # Wait 20 seconds to receive data
        logging.info("Waiting 20 seconds to receive sensor data...")
        time.sleep(20)

        # Close LiDAR
        status = controller.close_lidar()
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "Failed to close LiDAR, code: %s, message: %s",
                status.code,
                status.message,
            )
            robot.shutdown()
            return -1

        logging.info("LiDAR closed successfully")

        return 0

    except Exception as e:
        logging.error("Exception occurred during program execution: %s", e)
        return -1

    finally:
        # Clean up resources
        try:
            logging.info("Clean up resources")
            # Close sensor controller
            sensor_controller = robot.get_sensor_controller()
            sensor_controller.shutdown()
            logging.info("Sensor controller closed")

            # Disconnect
            robot.disconnect()
            logging.info("Robot connection disconnected")

            # Shutdown robot
            robot.shutdown()
            logging.info("Robot shutdown")

        except Exception as e:
            logging.error("Exception occurred while cleaning up resources: %s", e)


if __name__ == "__main__":
    sys.exit(main())
