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
running = True

body_imu_counter = 0
arm_state_counter = 0
leg_state_counter = 0
head_state_counter = 0
waist_state_counter = 0


def signal_handler(signum, frame):
    """Signal handler function for graceful exit"""
    global robot, running
    running = False
    logging.info("Received interrupt signal (%s), exiting...", signum)
    if robot:
        robot.disconnect()
        logging.info("Robot disconnected")
        robot.shutdown()
        logging.info("Robot shutdown")
    exit(-1)


def body_imu_callback(imu_data):
    """Body IMU data callback function"""
    global body_imu_counter
    if body_imu_counter % 1000 == 0:
        logging.info("+++++++++++++ Received body IMU data")
        # Print IMU data
        logging.info("Received body IMU data, timestamp: %d", imu_data.timestamp)
        logging.info("Received body IMU data, orientation: %s", imu_data.orientation)
        logging.info(
            "Received body IMU data, angular_velocity: %s",
            imu_data.angular_velocity,
        )
        logging.info(
            "Received body IMU data, linear_acceleration: %s",
            imu_data.linear_acceleration,
        )
        logging.info("Received body IMU data, temperature: %s", imu_data.temperature)
    body_imu_counter += 1


def arm_state_callback(joint_state):
    """Arm joint state callback function"""
    global arm_state_counter
    if arm_state_counter % 1000 == 0:
        logging.info("+++++++++++++ Received arm joint state data")
        # Print joint state data
        logging.info(
            "Received arm joint state data, status_word: %d",
            joint_state.joints[0].status_word,
        )
        logging.info(
            "Received arm joint state data, posH: %s", joint_state.joints[0].posH
        )
        logging.info(
            "Received arm joint state data, posL: %s", joint_state.joints[0].posL
        )
        logging.info(
            "Received arm joint state data, vel: %s", joint_state.joints[0].vel
        )
        logging.info(
            "Received arm joint state data, toq: %s", joint_state.joints[0].toq
        )
        logging.info(
            "Received arm joint state data, current: %s", joint_state.joints[0].current
        )
        logging.info(
            "Received arm joint state data, error_code: %s",
            joint_state.joints[0].err_code,
        )
    arm_state_counter += 1


def leg_state_callback(joint_state):
    """Leg joint state callback function"""
    global leg_state_counter
    if leg_state_counter % 1000 == 0:
        logging.info("+++++++++++++ Received leg joint state data")
        # Print joint state data
        logging.info(
            "Received leg joint state data, status_word: %d",
            joint_state.joints[0].status_word,
        )
        logging.info(
            "Received leg joint state data, posH: %s", joint_state.joints[0].posH
        )
        logging.info(
            "Received leg joint state data, posL: %s", joint_state.joints[0].posL
        )
        logging.info(
            "Received leg joint state data, vel: %s", joint_state.joints[0].vel
        )
        logging.info(
            "Received leg joint state data, toq: %s", joint_state.joints[0].toq
        )
        logging.info(
            "Received leg joint state data, current: %s", joint_state.joints[0].current
        )
        logging.info(
            "Received leg joint state data, error_code: %s",
            joint_state.joints[0].err_code,
        )
    leg_state_counter += 1


def head_state_callback(joint_state):
    """Head joint state callback function"""
    global head_state_counter
    if head_state_counter % 1000 == 0:
        logging.info("+++++++++++++ Received head joint state data")
        # Print joint state data
        logging.info(
            "Received head joint state data, status_word: %d",
            joint_state.joints[0].status_word,
        )
        logging.info(
            "Received head joint state data, posH: %s", joint_state.joints[0].posH
        )
        logging.info(
            "Received head joint state data, posL: %s", joint_state.joints[0].posL
        )
        logging.info(
            "Received head joint state data, vel: %s", joint_state.joints[0].vel
        )
        logging.info(
            "Received head joint state data, toq: %s", joint_state.joints[0].toq
        )
        logging.info(
            "Received head joint state data, current: %s", joint_state.joints[0].current
        )
        logging.info(
            "Received head joint state data, error_code: %s",
            joint_state.joints[0].err_code,
        )
    head_state_counter += 1


def waist_state_callback(joint_state):
    """Waist joint state callback function"""
    global waist_state_counter
    if waist_state_counter % 1000 == 0:
        logging.info("+++++++++++++ Received waist joint state data")
        # Print joint state data
        logging.info(
            "Received waist joint state data, status_word: %d",
            joint_state.joints[0].status_word,
        )
        logging.info(
            "Received waist joint state data, posH: %s", joint_state.joints[0].posH
        )
        logging.info(
            "Received waist joint state data, posL: %s", joint_state.joints[0].posL
        )
        logging.info(
            "Received waist joint state data, vel: %s", joint_state.joints[0].vel
        )
        logging.info(
            "Received waist joint state data, toq: %s", joint_state.joints[0].toq
        )
        logging.info(
            "Received waist joint state data, current: %s",
            joint_state.joints[0].current,
        )
        logging.info(
            "Received waist joint state data, error_code: %s",
            joint_state.joints[0].err_code,
        )
    waist_state_counter += 1


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

        # Set RPC timeout to 10 seconds
        robot.set_timeout(10000)

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

        # Subscribe to leg joint state
        controller.subscribe_leg_state(leg_state_callback)
        logging.info("Subscribed to leg joint state")

        # Subscribe to head joint state
        controller.subscribe_head_state(head_state_callback)
        logging.info("Subscribed to head joint state")

        # Subscribe to waist joint state
        controller.subscribe_waist_state(waist_state_callback)
        logging.info("Subscribed to waist joint state")

        # Main loop
        global running
        while running:
            # Create arm joint control command
            arm_command = magicbot.JointCommand()
            leg_command = magicbot.JointCommand()
            waist_command = magicbot.JointCommand()
            head_command = magicbot.JointCommand()

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

            for i in range(magicbot.LEG_JOINT_NUM):
                joint = magicbot.SingleJointCommand()
                joint.operation_mode = 200  # Preparation state
                joint.pos = 0.0
                joint.vel = 0.0
                joint.toq = 0.0
                joint.kp = 0.0
                joint.kd = 0.0
                leg_command.joints.append(joint)

            for i in range(magicbot.HEAD_JOINT_NUM):
                joint = magicbot.SingleJointCommand()
                joint.operation_mode = 200  # Preparation state
                joint.pos = 0.0
                joint.vel = 0.0
                joint.toq = 0.0
                joint.kp = 0.0
                joint.kd = 0.0
                head_command.joints.append(joint)

            for i in range(magicbot.WAIST_JOINT_NUM):
                joint = magicbot.SingleJointCommand()
                joint.operation_mode = 200  # Preparation state
                joint.pos = 0.0
                joint.vel = 0.0
                joint.toq = 0.0
                joint.kp = 0.0
                joint.kd = 0.0
                waist_command.joints.append(joint)

            # Publish arm joint control command
            controller.publish_arm_command(arm_command)

            # Publish leg joint control command
            controller.publish_leg_command(leg_command)

            # Publish waist joint control command
            controller.publish_waist_command(waist_command)

            # Publish head joint control command
            controller.publish_head_command(head_command)

            time.sleep(0.002)

    except Exception as e:
        logging.error("Exception occurred during program execution: %s", e)
        return -1

    finally:
        # Clean up resources
        try:
            logging.info("Clean up resources")
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
