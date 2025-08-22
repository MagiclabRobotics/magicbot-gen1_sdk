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
    logging.info("Received interrupt signal (%s), exiting...", signum)
    if robot:
        robot.disconnect()
        robot.shutdown()


def body_imu_callback(imu_data):
    """Body IMU data callback function"""
    logging.info("Received body IMU data")
    # TODO: Process body IMU data


def arm_state_callback(joint_state):
    """Arm joint state callback function"""
    logging.info("Received arm joint state data")
    # TODO: Process arm joint state data


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

        # Switch motion control controller to low-level controller, default is high-level controller
        status = robot.set_motion_control_level(magicbot.ControllerLevel.LowLevel)
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "Failed to switch robot motion control level, code: %s, message: %s",
                status.code,
                status.message,
            )
            robot.shutdown()
            return -1

        logging.info("Switched to low-level motion controller")

        # Get low-level motion controller
        controller = robot.get_low_level_motion_controller()

        # Set control command sending period to 2ms, 500Hz
        controller.set_period_ms(2)
        logging.info("Set control period to 2ms (500Hz)")

        # Subscribe to body IMU data
        controller.subscribe_body_imu(body_imu_callback)
        logging.info("Subscribed to body IMU data")

        # Subscribe to arm joint state
        controller.subscribe_arm_state(arm_state_callback)
        logging.info("Subscribed to arm joint state")

        # Create arm joint control command
        arm_command = magicbot.JointCommand()
        arm_command.joints = []

        # Set all joints to preparation state (operation mode 200)
        for i in range(magicbot.ARM_JOINT_NUM):
            joint = magicbot.SingleJointCommand()
            joint.operation_mode = 200  # Preparation state
            joint.pos = 0.0
            joint.vel = 0.0
            joint.toq = 0.0
            joint.kp = 0.0
            joint.kd = 0.0
            arm_command.joints.append(joint)

        # Publish arm joint control command
        controller.publish_arm_command(arm_command)
        logging.info(
            "Published arm joint preparation state command, joint count: %d",
            len(arm_command.joints),
        )

        # Wait 100 seconds
        logging.info("Waiting 100 seconds...")
        time.sleep(100)

        return 0

    except Exception as e:
        logging.error("Exception occurred during program execution: %s", e)
        return -1

    finally:
        # Clean up resources
        try:
            # Close low-level motion controller
            controller = robot.get_low_level_motion_controller()
            controller.shutdown()
            logging.info("Low-level motion controller closed")

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
