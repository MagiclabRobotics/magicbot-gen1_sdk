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


def signal_handler(signum, frame):
    """Signal handler function for graceful exit"""
    global running, robot
    logging.info("Received interrupt signal (%s), exiting...", signum)
    running = False
    if robot:
        robot.disconnect()
        robot.shutdown()


def print_help():
    """Print help information"""
    logging.info("High-Level Motion Control Function Demo Program")
    logging.info("")
    logging.info("Key Function Description:")
    logging.info("  ESC      Exit program")
    logging.info("  1        Function 1: Recovery stand")
    logging.info("  2        Function 2: Balance stand")
    logging.info("  3        Function 3: Execute trick - celebrate action")
    logging.info("  w        Function 4: Move forward")
    logging.info("  a        Function 5: Move left")
    logging.info("  s        Function 6: Move backward")
    logging.info("  d        Function 7: Move right")
    logging.info("  t        Function 8: Turn left")
    logging.info("  g        Function 9: Turn right")
    logging.info("  4        Function 10: Get current gait")
    logging.info("  5        Function 11: Execute handshake action")
    logging.info("  6        Function 12: Execute nod action")
    logging.info("  7        Function 13: Execute shake head action")
    logging.info("  8        Function 14: Execute greeting action")


def get_user_input():
    """Get user input"""
    try:
        # Python implementation of getch() on Linux systems
        import tty
        import termios

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    except ImportError:
        # If termios is not available, use simple input
        return input("Please press a key: ").strip()


def recovery_stand():
    """Recovery stand"""
    global robot
    try:
        logging.info("=== Executing Recovery Stand ===")

        # Get high-level motion controller
        controller = robot.get_high_level_motion_controller()

        # Set gait to recovery stand
        status = controller.set_gait(magicbot.GaitMode.GAIT_RECOVERY_STAND)
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "Failed to set robot gait, code: %s, message: %s",
                status.code,
                status.message,
            )
            return False

        logging.info("Robot gait set to recovery stand")
        return True

    except Exception as e:
        logging.error("Exception occurred while executing recovery stand: %s", e)
        return False


def balance_stand():
    """Balance stand"""
    global robot
    try:
        logging.info("=== Executing Balance Stand ===")

        # Get high-level motion controller
        controller = robot.get_high_level_motion_controller()

        # Set gait to balance stand
        status = controller.set_gait(magicbot.GaitMode.GAIT_BALANCE_STAND)
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "Failed to set robot gait, code: %s, message: %s",
                status.code,
                status.message,
            )
            return False

        logging.info("Robot gait set to balance stand (supports movement)")
        return True

    except Exception as e:
        logging.error("Exception occurred while executing balance stand: %s", e)
        return False


def execute_trick_celebrate():
    """Execute trick - celebrate action"""
    global robot
    try:
        logging.info("=== Executing Trick - Celebrate Action ===")

        # Get high-level motion controller
        controller = robot.get_high_level_motion_controller()

        # Execute celebrate trick
        status = controller.execute_trick(magicbot.TrickAction.ACTION_CELEBRATE)
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "Failed to execute robot trick, code: %s, message: %s",
                status.code,
                status.message,
            )
            return False

        logging.info("Robot trick executed successfully")
        return True

    except Exception as e:
        logging.error("Exception occurred while executing trick: %s", e)
        return False


def execute_trick_handshake():
    """Execute trick - handshake action"""
    global robot
    try:
        logging.info("=== Executing Trick - Handshake Action ===")

        # Get high-level motion controller
        controller = robot.get_high_level_motion_controller()

        # Execute handshake trick
        status = controller.execute_trick(
            magicbot.TrickAction.ACTION_SHAKE_HAND_REACHOUT
        )
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "Failed to execute robot trick, code: %s, message: %s",
                status.code,
                status.message,
            )
            return False

        logging.info("Robot handshake trick executed successfully")
        return True

    except Exception as e:
        logging.error("Exception occurred while executing trick: %s", e)
        return False


def execute_trick_nod():
    """Execute trick - nod action"""
    global robot
    try:
        logging.info("=== Executing Trick - Nod Action ===")

        # Get high-level motion controller
        controller = robot.get_high_level_motion_controller()

        # Execute nod trick
        status = controller.execute_trick(magicbot.TrickAction.ACTION_NOD_HEAD)
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "Failed to execute robot trick, code: %s, message: %s",
                status.code,
                status.message,
            )
            return False

        logging.info("Robot nod trick executed successfully")
        return True

    except Exception as e:
        logging.error("Exception occurred while executing trick: %s", e)
        return False


def execute_trick_shake_head():
    """Execute trick - shake head action"""
    global robot
    try:
        logging.info("=== Executing Trick - Shake Head Action ===")

        # Get high-level motion controller
        controller = robot.get_high_level_motion_controller()

        # Execute shake head trick
        status = controller.execute_trick(magicbot.TrickAction.ACTION_SHAKE_HEAD)
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "Failed to execute robot trick, code: %s, message: %s",
                status.code,
                status.message,
            )
            return False

        logging.info("Robot shake head trick executed successfully")
        return True

    except Exception as e:
        logging.error("Exception occurred while executing trick: %s", e)
        return False


def execute_trick_greeting():
    """Execute trick - greeting action"""
    global robot
    try:
        logging.info("=== Executing Trick - Greeting Action ===")

        # Get high-level motion controller
        controller = robot.get_high_level_motion_controller()

        # Execute greeting trick
        status = controller.execute_trick(magicbot.TrickAction.ACTION_GTEETING)
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "Failed to execute robot trick, code: %s, message: %s",
                status.code,
                status.message,
            )
            return False

        logging.info("Robot greeting trick executed successfully")
        return True

    except Exception as e:
        logging.error("Exception occurred while executing trick: %s", e)
        return False


def get_current_gait():
    """Get current gait"""
    global robot
    try:
        logging.info("=== Getting Current Gait ===")

        # Get high-level motion controller
        controller = robot.get_high_level_motion_controller()

        # Get current gait
        status, gait_mode = controller.get_gait()
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "Failed to get robot gait, code: %s, message: %s",
                status.code,
                status.message,
            )
            return False

        # Get gait names
        gait_names = {
            magicbot.GaitMode.GAIT_PASSIVE: "Idle mode",
            magicbot.GaitMode.GAIT_RECOVERY_STAND: "Recovery stand",
            magicbot.GaitMode.GAIT_CLASSIC_WALK: "Classic walk",
            magicbot.GaitMode.GAIT_PURE_DAMPER: "Damping mode",
            magicbot.GaitMode.GAIT_HUMANOID_WALK: "Humanoid walk",
            magicbot.GaitMode.GAIT_ALL_TERRAIN_WALK: "All-terrain walk",
            magicbot.GaitMode.GAIT_FAST_WALK: "Fast walk",
            magicbot.GaitMode.GAIT_SQUAT: "Squat",
            magicbot.GaitMode.GAIT_BALANCE_STAND: "Balance stand (supports movement)",
            magicbot.GaitMode.GAIT_ARM_SWING_WALK: "Arm swing walk",
            magicbot.GaitMode.GAIT_HUMANOID_RUN: "Humanoid run",
            magicbot.GaitMode.GAIT_LOWLEVL_SDK: "Low-level SDK mode",
        }

        gait_name = gait_names.get(gait_mode, f"Unknown gait({gait_mode})")
        logging.info("Current gait: %s", gait_name)
        return True

    except Exception as e:
        logging.error("Exception occurred while getting current gait: %s", e)
        return False


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
                "Failed to send joystick command, code: %s, message: %s",
                status.code,
                status.message,
            )
            time.sleep(0.05)  # Wait 50ms
            return False

        # Wait 50ms
        time.sleep(0.05)
        return True

    except Exception as e:
        logging.error("Exception occurred while sending joystick command: %s", e)
        return False


def move_forward():
    """Move forward"""
    logging.info("=== Moving Forward ===")
    return joystick_command(0.0, 1.0, 0.0, 0.0)


def move_backward():
    """Move backward"""
    logging.info("=== Moving Backward ===")
    return joystick_command(0.0, -1.0, 0.0, 0.0)


def move_left():
    """Move left"""
    logging.info("=== Moving Left ===")
    return joystick_command(-1.0, 0.0, 0.0, 0.0)


def move_right():
    """Move right"""
    logging.info("=== Moving Right ===")
    return joystick_command(1.0, 0.0, 0.0, 0.0)


def turn_left():
    """Turn left"""
    logging.info("=== Turning Left ===")
    return joystick_command(0.0, 0.0, -1.0, 0.0)


def turn_right():
    """Turn right"""
    logging.info("=== Turning Right ===")
    return joystick_command(0.0, 0.0, 1.0, 0.0)


def demo_all_high_level_functions():
    """Demo all high-level motion control functions"""
    logging.info("=== Demo All High-Level Motion Control Functions ===")

    success_count = 0
    total_tests = 6

    # Test recovery stand
    if recovery_stand():
        success_count += 1
        time.sleep(2)

    # Test balance stand
    if balance_stand():
        success_count += 1
        time.sleep(2)

    # Test get current gait
    if get_current_gait():
        success_count += 1
        time.sleep(1)

    # Test celebrate trick
    if execute_trick_celebrate():
        success_count += 1
        time.sleep(3)

    # Test handshake trick
    if execute_trick_handshake():
        success_count += 1
        time.sleep(3)

    # Test nod trick
    if execute_trick_nod():
        success_count += 1
        time.sleep(2)

    logging.info(
        "High-level motion control function test completed: %s/%s functions tested successfully",
        success_count,
        total_tests,
    )
    return success_count == total_tests


def main():
    """Main function"""
    global robot, running

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

        # Set RPC timeout to 5 seconds
        robot.set_timeout(5000)

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

        # Switch motion control controller to high-level controller
        status = robot.set_motion_control_level(magicbot.ControllerLevel.HighLevel)
        if status.code != magicbot.ErrorCode.OK:
            logging.error(
                "Failed to switch robot motion control level, code: %s, message: %s",
                status.code,
                status.message,
            )
            robot.shutdown()
            return -1

        logging.info("Switched to high-level motion controller")

        # Initialize high-level motion controller
        controller = robot.get_high_level_motion_controller()
        if not controller.initialize():
            logging.error("Failed to initialize high-level motion controller")
            robot.disconnect()
            robot.shutdown()
            return -1

        logging.info("Successfully initialized high-level motion controller")

        print_help()
        logging.info("Press any key to continue (ESC to exit)...")

        # Main loop
        while running:
            try:
                key = get_user_input()

                if key == "\x1b":  # ESC key
                    break

                logging.info("Key pressed: %s", key)

                if key == "1":
                    recovery_stand()
                elif key == "2":
                    balance_stand()
                elif key == "3":
                    execute_trick_celebrate()
                elif key == "4":
                    get_current_gait()
                elif key == "5":
                    execute_trick_handshake()
                elif key == "6":
                    execute_trick_nod()
                elif key == "7":
                    execute_trick_shake_head()
                elif key == "8":
                    execute_trick_greeting()
                elif key == "w":
                    move_forward()
                elif key == "a":
                    move_left()
                elif key == "s":
                    move_backward()
                elif key == "d":
                    move_right()
                elif key == "t":
                    turn_left()
                elif key == "g":
                    turn_right()
                else:
                    logging.info("Unknown key: %s", key)

                time.sleep(0.01)  # Brief delay

            except KeyboardInterrupt:
                break
            except Exception as e:
                logging.error("Exception occurred while processing user input: %s", e)

        return 0

    except Exception as e:
        logging.error("Exception occurred during program execution: %s", e)
        return -1

    finally:
        # Clean up resources
        try:
            # Close high-level motion controller
            controller = robot.get_high_level_motion_controller()
            controller.shutdown()
            logging.info("High-level motion controller closed")

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
