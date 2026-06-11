#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import signal
import logging
import termios
import tty
import gc
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

# Static variable for position increment
pos = 0.0

# Counters for controlling print frequency
upper_body_state_counter = 0
all_hand_state_counter = 0


def signal_handler(signum, frame):
    """Signal handler function for graceful exit"""
    global running, robot
    logging.info("Received interrupt signal (%s), exiting...", signum)
    running = False
    if robot:
        robot.shutdown()
        logging.info("Robot shutdown")
    exit(signum)


def print_help():
    """Print help information"""
    logging.info("Key Function Description:")
    logging.info("Gait and Trick Functions:")
    logging.info("  0        Function 0: Get gait")
    logging.info("  1        Function 1: Set recovery stand gait")
    logging.info("  2        Function 2: Set hybrid gait")
    logging.info("")
    logging.info("Joystick Functions:")
    logging.info("  w        Function w: Move forward")
    logging.info("  a        Function a: Move left")
    logging.info("  s        Function s: Move backward")
    logging.info("  d        Function d: Move right")
    logging.info("  x        Function x: Stop")
    logging.info("  t        Function t: Turn left")
    logging.info("  g        Function g: Turn right")
    logging.info("")
    logging.info("Upper Body Functions:")
    logging.info("  3        Function 3: Subscribe upper body state")
    logging.info("  4        Function 4: Unsubscribe upper body state")
    logging.info("  5        Function 5: Publish upper body command")
    logging.info("  6        Function 6: Subscribe all hand state")
    logging.info("  7        Function 7: Unsubscribe all hand state")
    logging.info("  8        Function 8: Publish all hand command")
    logging.info("")
    logging.info("  ESC      Exit program")
    logging.info("  ?        Function ?: Print help")


def getch():
    """Get single character input (no echo)"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, old_settings)
    return ch


def get_gait():
    """Get current gait mode"""
    global robot
    try:
        # Get high-level motion controller
        controller = robot.get_high_level_motion_controller()

        # Get gait
        status, gait_mode = controller.get_gait()
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "get robot gait failed, code: %s, message: %s",
                status.code,
                status.message,
            )
            return
        logging.info("robot gait: %s", int(gait_mode))

    except Exception as e:
        logging.error("Exception occurred while getting gait: %s", e)


def set_recovery_stand_gait():
    """Set recovery stand gait"""
    global robot
    try:
        # Get high-level motion controller
        controller = robot.get_high_level_motion_controller()

        # Set gait
        status = controller.set_gait(magicbot.GaitMode.GAIT_RECOVERY_STAND, 10000)
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "set robot gait failed, code: %s, message: %s",
                status.code,
                status.message,
            )
            return
        logging.info("robot gait set to GAIT_RECOVERY_STAND successfully.")

    except Exception as e:
        logging.error("Exception occurred while setting recovery stand gait: %s", e)


def set_hybrid_gait():
    """Set hybrid gait"""
    global robot
    try:
        # Get high-level motion controller
        controller = robot.get_high_level_motion_controller()

        # Set gait
        status = controller.set_gait(magicbot.GaitMode.GAIT_HYBRID_SDK, 10000)
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "set robot gait failed, code: %s, message: %s",
                status.code,
                status.message,
            )
            return
        logging.info("robot gait set to GAIT_HYBRID_SDK successfully.")

    except Exception as e:
        logging.error("Exception occurred while setting hybrid gait: %s", e)


def joystick_command(left_x_axis, left_y_axis, right_x_axis, right_y_axis):
    """Send joystick control command"""
    global robot
    try:
        # Get high-level motion controller
        controller = robot.get_high_level_motion_controller()

        # Create joystick command
        joy_command = magicbot.JoystickCommand()
        joy_command.left_x_axis = left_x_axis
        joy_command.left_y_axis = left_y_axis
        joy_command.right_x_axis = right_x_axis
        joy_command.right_y_axis = right_y_axis

        # Send joystick command
        status = controller.send_joystick_command(joy_command)
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "execute robot trick failed, code: %s, message: %s",
                status.code,
                status.message,
            )
            time.sleep(0.05)
            return
        # Wait 50ms
        time.sleep(0.05)

    except Exception as e:
        logging.error("Exception occurred while sending joystick command: %s", e)


def subscribe_upper_body_state():
    """Subscribe to upper body state"""
    global robot
    try:
        # Get upper body motion controller
        controller = robot.get_upper_body_motion_controller()

        # Unsubscribe first to ensure clean state
        try:
            controller.unsubscribe_upper_body_state()
            # Force garbage collection to release Python callback references
            gc.collect()
            # Wait longer to ensure C++ cleanup completes
            time.sleep(0.5)
        except Exception:
            pass  # Ignore if not subscribed

        def upper_body_state_callback(joint_state):
            """Upper body state callback function"""
            global upper_body_state_counter
            upper_body_state_counter += 1
            # Print every 100 callbacks to reduce output frequency
            if upper_body_state_counter % 100 == 0:
                logging.info("upper body state timestamp: %d", joint_state.timestamp)
                for ii in range(len(joint_state.joints)):
                    joint = joint_state.joints[ii]
                    logging.info(
                        "upper body state joint %d status_word: %d, posH: %s, posL: %s, vel: %s, toq: %s, current: %s, err_code: %s",
                        ii,
                        joint.status_word,
                        joint.posH,
                        joint.posL,
                        joint.vel,
                        joint.toq,
                        joint.current,
                        joint.err_code,
                    )
                logging.info("--------------------------------")

        # Subscribe to upper body state
        controller.subscribe_upper_body_state(upper_body_state_callback)
        logging.info("Subscribed to upper body state")

    except Exception as e:
        logging.error("Exception occurred while subscribing upper body state: %s", e)


def unsubscribe_upper_body_state():
    """Unsubscribe from upper body state"""
    global robot
    try:
        # Get upper body motion controller
        controller = robot.get_upper_body_motion_controller()

        # Unsubscribe from upper body state
        controller.unsubscribe_upper_body_state()
        # Force garbage collection to release Python callback references
        gc.collect()
        # Wait a bit to ensure cleanup
        time.sleep(0.2)
        logging.info("Unsubscribed from upper body state")

    except Exception as e:
        logging.error("Exception occurred while unsubscribing upper body state: %s", e)


def publish_upper_body_command():
    """Publish upper body command"""
    global robot, pos
    try:
        # Get upper body motion controller
        controller = robot.get_upper_body_motion_controller()

        # Create joint command
        command = magicbot.JointCommand()
        command.timestamp = int(time.time() * 1e9)  # nanoseconds
        command.motion_mode = 1

        # Increment position
        # pos += 0.001

        # Create 18 joints
        for ii in range(18):
            joint = magicbot.SingleJointCommand()
            joint.operation_mode = 4
            joint.pos = pos
            joint.vel = 0.0
            joint.toq = 0.0
            joint.kp = 0.0
            joint.kd = 0.0
            command.joints.append(joint)
        
        command.joints[0].pos = 0.01
        command.joints[1].pos = 0.11
        command.joints[2].pos = 1.18
        command.joints[3].pos = -0.51
        command.joints[4].pos = -1.49
        command.joints[5].pos = 0.0
        command.joints[6].pos = 0.0

        command.joints[7].pos = 0.01
        command.joints[8].pos = -0.11
        command.joints[9].pos = -1.18
        command.joints[10].pos = 0.51
        command.joints[11].pos = 1.49
        command.joints[12].pos = 0.0
        command.joints[13].pos = 0.0

        command.joints[14].pos = 0.0
        command.joints[15].pos = 0.0
        command.joints[16].pos = 0.0
        command.joints[17].pos = 0.0
        
        command.joints[0].kp = 5.0
        command.joints[0].kd = 40.0
        command.joints[1].kp = 5.0
        command.joints[1].kd = 40.0

        command.joints[2].kp = 10.0
        command.joints[2].kd = 25.0
        command.joints[3].kp = 10.0
        command.joints[3].kd = 25.0
        command.joints[4].kp = 10.0
        command.joints[4].kd = 25.0
        command.joints[5].kp = 10.0
        command.joints[5].kd = 25.0
        command.joints[6].kp = 10.0
        command.joints[6].kd = 25.0

        command.joints[7].kp = 5.0
        command.joints[7].kd = 40.0
        command.joints[8].kp = 5.0
        command.joints[8].kd = 40.0

        command.joints[9].kp = 10.0
        command.joints[9].kd = 25.0
        command.joints[10].kp = 10.0
        command.joints[10].kd = 25.0
        command.joints[11].kp = 10.0
        command.joints[11].kd = 25.0
        command.joints[12].kp = 10.0
        command.joints[12].kd = 25.0
        command.joints[13].kp = 10.0
        command.joints[13].kd = 25.0

        command.joints[14].kp = 50.0
        command.joints[14].kd = 200.0
        command.joints[15].kp = 50.0
        command.joints[15].kd = 200.0

        command.joints[16].kp = 250.0
        command.joints[16].kd = 10.0
        command.joints[17].kp = 250.0
        command.joints[17].kd = 10.0


        # Publish upper body command
        status = controller.publish_upper_body_command(command)
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "publish upper body command failed, code: %s, message: %s",
                status.code,
                status.message,
            )
            return
        logging.info(status.message)

    except Exception as e:
        logging.error("Exception occurred while publishing upper body command: %s", e)


def subscribe_all_hand_state():
    """Subscribe to all hand state"""
    global robot
    try:
        # Get upper body motion controller
        controller = robot.get_upper_body_motion_controller()

        # Unsubscribe first to ensure clean state
        try:
            controller.unsubscribe_all_hand_state()
            # Force garbage collection to release Python callback references
            gc.collect()
            # Wait longer to ensure C++ cleanup completes
            time.sleep(0.5)
        except Exception:
            pass  # Ignore if not subscribed

        def all_hand_state_callback(all_hand_state):
            """All hand state callback function"""
            global all_hand_state_counter
            all_hand_state_counter += 1
            # Print every 100 callbacks to reduce output frequency
            if all_hand_state_counter % 100 == 0:
                logging.info("all hand state timestamp: %d", all_hand_state.timestamp)
                for ii in range(len(all_hand_state.state)):
                    for jj in range(len(all_hand_state.state[ii].status_word)):
                        logging.info(
                            "all hand state hand %d status_word %d: %d",
                            ii,
                            jj,
                            all_hand_state.state[ii].status_word[jj],
                        )
                    for jj in range(len(all_hand_state.state[ii].pos)):
                        logging.info(
                            "all hand state hand %d pos %d: %s",
                            ii,
                            jj,
                            all_hand_state.state[ii].pos[jj],
                        )
                    for jj in range(len(all_hand_state.state[ii].toq)):
                        logging.info(
                            "all hand state hand %d toq %d: %s",
                            ii,
                            jj,
                            all_hand_state.state[ii].toq[jj],
                        )
                    for jj in range(len(all_hand_state.state[ii].cur)):
                        logging.info(
                            "all hand state hand %d cur %d: %s",
                            ii,
                            jj,
                            all_hand_state.state[ii].cur[jj],
                        )
                    for jj in range(len(all_hand_state.state[ii].error_code)):
                        logging.info(
                            "all hand state hand %d error_code %d: %s",
                            ii,
                            jj,
                            all_hand_state.state[ii].error_code[jj],
                        )
                logging.info("--------------------------------")

        # Subscribe to all hand state
        controller.subscribe_all_hand_state(all_hand_state_callback)
        logging.info("Subscribed to all hand state")

    except Exception as e:
        logging.error("Exception occurred while subscribing all hand state: %s", e)


def unsubscribe_all_hand_state():
    """Unsubscribe from all hand state"""
    global robot
    try:
        # Get upper body motion controller
        controller = robot.get_upper_body_motion_controller()

        # Unsubscribe from all hand state
        controller.unsubscribe_all_hand_state()
        # Force garbage collection to release Python callback references
        gc.collect()
        # Wait a bit to ensure cleanup
        time.sleep(0.2)
        logging.info("Unsubscribed from all hand state")

    except Exception as e:
        logging.error("Exception occurred while unsubscribing all hand state: %s", e)


def publish_all_hand_command():
    """Publish all hand command"""
    global robot, pos
    try:
        # Get upper body motion controller
        controller = robot.get_upper_body_motion_controller()

        # Create hand command
        command = magicbot.HandCommand()
        command.timestamp = int(time.time() * 1e9)  # nanoseconds

        # Increment position
        # pos += 0.001

        # Create commands for all hands
        for ii in range(magicbot.HAND_NUM):
            single_hand_cmd = magicbot.SingleHandJointCommand()
            single_hand_cmd.operation_mode = 4
            for jj in range(magicbot.HAND_JOINT_NUM):
                single_hand_cmd.pos.append(pos)
            command.cmd.append(single_hand_cmd)
        
        command.cmd[0].pos[0] = 2.77
        command.cmd[0].pos[1] = 2.77
        command.cmd[0].pos[2] = 2.77
        command.cmd[0].pos[3] = 2.77
        command.cmd[0].pos[4] = 0.77
        command.cmd[0].pos[5] = 2.81
        
        command.cmd[1].pos[0] = 2.77
        command.cmd[1].pos[1] = 2.77
        command.cmd[1].pos[2] = 2.77
        command.cmd[1].pos[3] = 2.77
        command.cmd[1].pos[4] = 0.77
        command.cmd[1].pos[5] = 2.81

        # Publish all hand command
        controller.publish_all_hand_command(command)
        logging.info("Published all hand command")

    except Exception as e:
        logging.error("Exception occurred while publishing all hand command: %s", e)


def main():
    """Main function"""
    global robot, running

    # Set stdout to unbuffered to ensure output starts from line beginning
    sys.stdout.reconfigure(line_buffering=True)

    # Bind signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Configure local IP address for direct network connection and initialize SDK
    # local_ip = "192.168.54.111"
    local_ip = "127.0.0.1"
    robot = magicbot.MagicRobot()

    logging.info("SDK Version: %s", robot.get_sdk_version())

    print_help()

    try:
        if not robot.initialize(local_ip):
            logging.error("robot sdk initialize failed.")
            robot.shutdown()
            return -1

        # Connect to robot
        status = robot.connect()
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "connect robot failed, code: %s, message: %s",
                status.code,
                status.message,
            )
            robot.shutdown()
            return -1

        logging.info("Press any key to continue (ESC to exit)...")

        # Wait for user input
        while running:
            try:
                key = getch()
                if ord(key) == 27:  # ESC key ASCII code is 27
                    break

                logging.info("Key ASCII: %d, Character: %s", ord(key), key)

                # 1. Gait and Trick Functions
                if key == "0":
                    get_gait()
                elif key == "1":
                    set_recovery_stand_gait()
                elif key == "2":
                    set_hybrid_gait()
                # 2. Joystick Functions
                elif key.lower() == "w":
                    joystick_command(0.0, 1.0, 0.0, 0.0)  # Forward
                elif key.lower() == "a":
                    joystick_command(-1.0, 0.0, 0.0, 0.0)  # Left
                elif key.lower() == "s":
                    joystick_command(0.0, -1.0, 0.0, 0.0)  # Backward
                elif key.lower() == "d":
                    joystick_command(1.0, 0.0, 0.0, 0.0)  # Right
                elif key.lower() == "x":
                    joystick_command(0.0, 0.0, 0.0, 0.0)  # Stop
                elif key.lower() == "t":
                    joystick_command(0.0, 0.0, -1.0, 0.0)  # Turn left
                elif key.lower() == "g":
                    joystick_command(0.0, 0.0, 1.0, 0.0)  # Turn right
                # 3. Upper Body Functions
                elif key == "3":
                    subscribe_upper_body_state()
                elif key == "4":
                    unsubscribe_upper_body_state()
                elif key == "5":
                    publish_upper_body_command()
                elif key == "6":
                    subscribe_all_hand_state()
                elif key == "7":
                    unsubscribe_all_hand_state()
                elif key == "8":
                    publish_all_hand_command()
                elif key == "?":
                    print_help()
                else:
                    logging.info("Unknown key: %s", key)

                time.sleep(0.01)

            except KeyboardInterrupt:
                break
            except Exception as e:
                logging.error("Exception occurred while processing user input: %s", e)

        # Disconnect from robot
        status = robot.disconnect()
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "disconnect robot failed, code: %s, message: %s",
                status.code,
                status.message,
            )
            robot.shutdown()
            return -1

        robot.shutdown()

        return 0

    except Exception as e:
        logging.error("Exception occurred during program execution: %s", e)
        return -1

    finally:
        # Clean up resources
        try:
            if robot:
                robot.shutdown()
        except Exception as e:
            logging.error("Exception occurred while cleaning up resources: %s", e)


if __name__ == "__main__":
    sys.exit(main())
