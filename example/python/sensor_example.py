#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import logging
from typing import Optional, Dict
import magicbot_gen1_python as magicbot
from magicbot_gen1_python import ErrorCode


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

lidar_imu_counter = 0
lidar_pointcloud_counter = 0
head_rgbd_color_counter = 0
head_rgbd_color_camera_info_counter = 0
head_rgbd_depth_image_counter = 0
head_rgbd_depth_camera_info_counter = 0
waist_rgbd_color_counter = 0
waist_rgbd_color_camera_info_counter = 0
waist_rgbd_depth_image_counter = 0
waist_rgbd_depth_camera_info_counter = 0
trinocular_image_counter = 0


class SensorManager:
    """Manages sensor subscriptions for MagicBot Gen1"""

    def __init__(self, sensor_controller):
        self.sensor_controller = sensor_controller
        self.sensors_state = {
            "lidar": False,
            "head_rgbd_camera": False,
            "waist_rgbd_camera": False,
            "trinocular_camera": False,
        }
        self.subscriptions = {
            # LiDAR subscriptions
            "lidar_imu": False,
            "lidar_point_cloud": False,
            # Head RGBD subscriptions
            "head_rgbd_color_image": False,
            "head_rgbd_color_camera_info": False,
            "head_rgbd_depth_image": False,
            "head_rgbd_depth_camera_info": False,
            # Waist RGBD subscriptions
            "waist_rgbd_color_image": False,
            "waist_rgbd_color_camera_info": False,
            "waist_rgbd_depth_image": False,
            "waist_rgbd_depth_camera_info": False,
            # Trinocular camera subscriptions
            "trinocular_image": False,
        }

    # === LiDAR Control ===
    def open_lidar(self) -> bool:
        """Open LiDAR"""
        if self.sensors_state["lidar"]:
            logging.warning("LiDAR already opened")
            return True

        status = self.sensor_controller.open_lidar()
        if status.code != ErrorCode.OK:
            logging.error(f"Failed to open LiDAR: {status.message}")
            return False

        self.sensors_state["lidar"] = True
        logging.info("✓ LiDAR opened successfully")
        return True

    def close_lidar(self) -> bool:
        """Close LiDAR"""
        if not self.sensors_state["lidar"]:
            logging.warning("LiDAR already closed")
            return True

        # Unsubscribe if subscribed
        if self.subscriptions["lidar_imu"]:
            self.toggle_lidar_imu_subscription()
        if self.subscriptions["lidar_point_cloud"]:
            self.toggle_lidar_point_cloud_subscription()

        status = self.sensor_controller.close_lidar()
        if status.code != ErrorCode.OK:
            logging.error(f"Failed to close LiDAR: {status.message}")
            return False

        self.sensors_state["lidar"] = False
        logging.info("✓ LiDAR closed")
        return True

    # === Head RGBD Camera Control ===
    def open_head_rgbd_camera(self) -> bool:
        """Open head RGBD camera"""
        if self.sensors_state["head_rgbd_camera"]:
            logging.warning("Head RGBD camera already opened")
            return True

        status = self.sensor_controller.open_head_rgbd_camera()
        if status.code != ErrorCode.OK:
            logging.error(f"Failed to open head RGBD camera: {status.message}")
            return False

        self.sensors_state["head_rgbd_camera"] = True
        logging.info("✓ Head RGBD camera opened")
        return True

    def close_head_rgbd_camera(self) -> bool:
        """Close head RGBD camera"""
        if not self.sensors_state["head_rgbd_camera"]:
            logging.warning("Head RGBD camera already closed")
            return True

        # Unsubscribe all head RGBD subscriptions if subscribed
        if self.subscriptions["head_rgbd_color_image"]:
            self.toggle_head_rgbd_color_image_subscription()
        if self.subscriptions["head_rgbd_color_camera_info"]:
            self.toggle_head_rgbd_color_camera_info_subscription()
        if self.subscriptions["head_rgbd_depth_image"]:
            self.toggle_head_rgbd_depth_image_subscription()
        if self.subscriptions["head_rgbd_depth_camera_info"]:
            self.toggle_head_rgbd_depth_camera_info_subscription()

        status = self.sensor_controller.close_head_rgbd_camera()
        if status.code != ErrorCode.OK:
            logging.error(f"Failed to close head RGBD camera: {status.message}")
            return False

        self.sensors_state["head_rgbd_camera"] = False
        logging.info("✓ Head RGBD camera closed")
        return True

    # === Waist RGBD Camera Control ===
    def open_waist_rgbd_camera(self) -> bool:
        """Open waist RGBD camera"""
        if self.sensors_state["waist_rgbd_camera"]:
            logging.warning("Waist RGBD camera already opened")
            return True

        status = self.sensor_controller.open_waist_rgbd_camera()
        if status.code != ErrorCode.OK:
            logging.error(f"Failed to open waist RGBD camera: {status.message}")
            return False

        self.sensors_state["waist_rgbd_camera"] = True
        logging.info("✓ Waist RGBD camera opened")
        return True

    def close_waist_rgbd_camera(self) -> bool:
        """Close waist RGBD camera"""
        if not self.sensors_state["waist_rgbd_camera"]:
            logging.warning("Waist RGBD camera already closed")
            return True

        # Unsubscribe all waist RGBD subscriptions if subscribed
        if self.subscriptions["waist_rgbd_color_image"]:
            self.toggle_waist_rgbd_color_image_subscription()
        if self.subscriptions["waist_rgbd_color_camera_info"]:
            self.toggle_waist_rgbd_color_camera_info_subscription()
        if self.subscriptions["waist_rgbd_depth_image"]:
            self.toggle_waist_rgbd_depth_image_subscription()
        if self.subscriptions["waist_rgbd_depth_camera_info"]:
            self.toggle_waist_rgbd_depth_camera_info_subscription()

        status = self.sensor_controller.close_waist_rgbd_camera()
        if status.code != ErrorCode.OK:
            logging.error(f"Failed to close waist RGBD camera: {status.message}")
            return False

        self.sensors_state["waist_rgbd_camera"] = False
        logging.info("✓ Waist RGBD camera closed")
        return True

    # === Trinocular Camera Control ===
    def open_trinocular_camera(self) -> bool:
        """Open trinocular camera"""
        if self.sensors_state["trinocular_camera"]:
            logging.warning("Trinocular camera already opened")
            return True

        status = self.sensor_controller.open_trinocular_camera()
        if status.code != ErrorCode.OK:
            logging.error(f"Failed to open trinocular camera: {status.message}")
            return False

        self.sensors_state["trinocular_camera"] = True
        logging.info("✓ Trinocular camera opened")
        return True

    def close_trinocular_camera(self) -> bool:
        """Close trinocular camera"""
        if not self.sensors_state["trinocular_camera"]:
            logging.warning("Trinocular camera already closed")
            return True

        # Unsubscribe if subscribed
        if self.subscriptions["trinocular_image"]:
            self.toggle_trinocular_image_subscription()

        status = self.sensor_controller.close_trinocular_camera()
        if status.code != ErrorCode.OK:
            logging.error(f"Failed to close trinocular camera: {status.message}")
            return False

        self.sensors_state["trinocular_camera"] = False
        logging.info("✓ Trinocular camera closed")
        return True

    # === LiDAR Subscribe/Unsubscribe Methods ===
    def toggle_lidar_imu_subscription(self):
        """Toggle LiDAR IMU subscription"""
        if self.subscriptions["lidar_imu"]:
            self.sensor_controller.unsubscribe_lidar_imu()
            self.subscriptions["lidar_imu"] = False
            logging.info("✓ LiDAR IMU unsubscribed")
        else:

            def lidar_imu_callback(imu):
                global lidar_imu_counter
                lidar_imu_counter += 1
                if lidar_imu_counter % 100 == 0:
                    logging.info(f"LiDAR IMU received (count: {lidar_imu_counter})")

            self.sensor_controller.subscribe_lidar_imu(lidar_imu_callback)
            self.subscriptions["lidar_imu"] = True
            logging.info("✓ LiDAR IMU subscribed")

    def toggle_lidar_point_cloud_subscription(self):
        """Toggle LiDAR point cloud subscription"""
        if self.subscriptions["lidar_point_cloud"]:
            self.sensor_controller.unsubscribe_lidar_point_cloud()
            self.subscriptions["lidar_point_cloud"] = False
            logging.info("✓ LiDAR point cloud unsubscribed")
        else:

            def lidar_pointcloud_callback(pointcloud):
                global lidar_pointcloud_counter
                lidar_pointcloud_counter += 1
                if lidar_pointcloud_counter % 10 == 0:
                    logging.info(
                        f"LiDAR Point Cloud: {len(pointcloud.data)} bytes (count: {lidar_pointcloud_counter})"
                    )

            self.sensor_controller.subscribe_lidar_point_cloud(
                lidar_pointcloud_callback
            )
            self.subscriptions["lidar_point_cloud"] = True
            logging.info("✓ LiDAR point cloud subscribed")

    # === Head RGBD Subscribe/Unsubscribe Methods ===
    def toggle_head_rgbd_color_image_subscription(self):
        """Toggle head RGBD color image subscription"""
        if self.subscriptions["head_rgbd_color_image"]:
            self.sensor_controller.unsubscribe_head_rgbd_color_image()
            self.subscriptions["head_rgbd_color_image"] = False
            logging.info("✓ Head RGBD color image unsubscribed")
        else:

            def head_rgbd_color_image_callback(img):
                global head_rgbd_color_counter
                head_rgbd_color_counter += 1
                if head_rgbd_color_counter % 15 == 0:
                    logging.info(
                        f"Head RGBD Color Image: {len(img.data)} bytes, {img.width}x{img.height} (count: {head_rgbd_color_counter})"
                    )

            self.sensor_controller.subscribe_head_rgbd_color_image(
                head_rgbd_color_image_callback
            )
            self.subscriptions["head_rgbd_color_image"] = True
            logging.info("✓ Head RGBD color image subscribed")

    def toggle_head_rgbd_color_camera_info_subscription(self):
        """Toggle head RGBD color camera info subscription"""
        if self.subscriptions["head_rgbd_color_camera_info"]:
            self.sensor_controller.unsubscribe_head_rgbd_color_camera_info()
            self.subscriptions["head_rgbd_color_camera_info"] = False
            logging.info("✓ Head RGBD color camera info unsubscribed")
        else:
            self.sensor_controller.subscribe_head_rgbd_color_camera_info(
                lambda info: logging.info(
                    f"Head RGBD Color Camera Info: {info.width}x{info.height}"
                )
            )
            self.subscriptions["head_rgbd_color_camera_info"] = True
            logging.info("✓ Head RGBD color camera info subscribed")

    def toggle_head_rgbd_depth_image_subscription(self):
        """Toggle head RGBD depth image subscription"""
        if self.subscriptions["head_rgbd_depth_image"]:
            self.sensor_controller.unsubscribe_head_rgbd_depth_image()
            self.subscriptions["head_rgbd_depth_image"] = False
            logging.info("✓ Head RGBD depth image unsubscribed")
        else:

            def head_rgbd_depth_image_callback(img):
                global head_rgbd_depth_image_counter
                head_rgbd_depth_image_counter += 1
                if head_rgbd_depth_image_counter % 15 == 0:
                    logging.info(
                        f"Head RGBD Depth Image: {len(img.data)} bytes, {img.width}x{img.height} (count: {head_rgbd_depth_image_counter})"
                    )

            self.sensor_controller.subscribe_head_rgbd_depth_image(
                head_rgbd_depth_image_callback
            )
            self.subscriptions["head_rgbd_depth_image"] = True
            logging.info("✓ Head RGBD depth image subscribed")

    def toggle_head_rgbd_depth_camera_info_subscription(self):
        """Toggle head RGBD depth camera info subscription"""
        if self.subscriptions["head_rgbd_depth_camera_info"]:
            self.sensor_controller.unsubscribe_head_rgbd_depth_camera_info()
            self.subscriptions["head_rgbd_depth_camera_info"] = False
            logging.info("✓ Head RGBD depth camera info unsubscribed")
        else:

            def head_rgbd_depth_camera_info_callback(info):
                global head_rgbd_depth_camera_info_counter
                head_rgbd_depth_camera_info_counter += 1
                if head_rgbd_depth_camera_info_counter % 15 == 0:
                    logging.info(
                        f"Head RGBD Depth Camera Info: {info.width}x{info.height} (count: {head_rgbd_depth_camera_info_counter})"
                    )

            self.sensor_controller.subscribe_head_rgbd_depth_camera_info(
                head_rgbd_depth_camera_info_callback
            )
            self.subscriptions["head_rgbd_depth_camera_info"] = True
            logging.info("✓ Head RGBD depth camera info subscribed")

    # === Waist RGBD Subscribe/Unsubscribe Methods ===
    def toggle_waist_rgbd_color_image_subscription(self):
        """Toggle waist RGBD color image subscription"""
        if self.subscriptions["waist_rgbd_color_image"]:
            self.sensor_controller.unsubscribe_waist_rgbd_color_image()
            self.subscriptions["waist_rgbd_color_image"] = False
            logging.info("✓ Waist RGBD color image unsubscribed")
        else:

            def waist_rgbd_color_image_callback(img):
                global waist_rgbd_color_counter
                waist_rgbd_color_counter += 1
                if waist_rgbd_color_counter % 15 == 0:
                    logging.info(
                        f"Waist RGBD Color Image: {len(img.data)} bytes, {img.width}x{img.height} (count: {waist_rgbd_color_counter})"
                    )

            self.sensor_controller.subscribe_waist_rgbd_color_image(
                waist_rgbd_color_image_callback
            )
            self.subscriptions["waist_rgbd_color_image"] = True
            logging.info("✓ Waist RGBD color image subscribed")

    def toggle_waist_rgbd_color_camera_info_subscription(self):
        """Toggle waist RGBD color camera info subscription"""
        if self.subscriptions["waist_rgbd_color_camera_info"]:
            self.sensor_controller.unsubscribe_waist_rgbd_color_camera_info()
            self.subscriptions["waist_rgbd_color_camera_info"] = False
            logging.info("✓ Waist RGBD color camera info unsubscribed")
        else:

            def waist_rgbd_color_camera_info_callback(info):
                global waist_rgbd_color_camera_info_counter
                waist_rgbd_color_camera_info_counter += 1
                if waist_rgbd_color_camera_info_counter % 15 == 0:
                    logging.info(
                        f"Waist RGBD Color Camera Info: {info.width}x{info.height} (count: {waist_rgbd_color_camera_info_counter})"
                    )

            self.sensor_controller.subscribe_waist_rgbd_color_camera_info(
                waist_rgbd_color_camera_info_callback
            )
            self.subscriptions["waist_rgbd_color_camera_info"] = True
            logging.info("✓ Waist RGBD color camera info subscribed")

    def toggle_waist_rgbd_depth_image_subscription(self):
        """Toggle waist RGBD depth image subscription"""
        if self.subscriptions["waist_rgbd_depth_image"]:
            self.sensor_controller.unsubscribe_waist_rgbd_depth_image()
            self.subscriptions["waist_rgbd_depth_image"] = False
            logging.info("✓ Waist RGBD depth image unsubscribed")
        else:

            def waist_rgbd_depth_image_callback(img):
                global waist_rgbd_depth_image_counter
                waist_rgbd_depth_image_counter += 1
                if waist_rgbd_depth_image_counter % 15 == 0:
                    logging.info(
                        f"Waist RGBD Depth Image: {len(img.data)} bytes, {img.width}x{img.height} (count: {waist_rgbd_depth_image_counter})"
                    )

            self.sensor_controller.subscribe_waist_rgbd_depth_image(
                waist_rgbd_depth_image_callback
            )
            self.subscriptions["waist_rgbd_depth_image"] = True
            logging.info("✓ Waist RGBD depth image subscribed")

    def toggle_waist_rgbd_depth_camera_info_subscription(self):
        """Toggle waist RGBD depth camera info subscription"""
        if self.subscriptions["waist_rgbd_depth_camera_info"]:
            self.sensor_controller.unsubscribe_waist_rgbd_depth_camera_info()
            self.subscriptions["waist_rgbd_depth_camera_info"] = False
            logging.info("✓ Waist RGBD depth camera info unsubscribed")
        else:

            def waist_rgbd_depth_camera_info_callback(info):
                global waist_rgbd_depth_camera_info_counter
                waist_rgbd_depth_camera_info_counter += 1
                if waist_rgbd_depth_camera_info_counter % 15 == 0:
                    logging.info(
                        f"Waist RGBD Depth Camera Info: {info.width}x{info.height} (count: {waist_rgbd_depth_camera_info_counter})"
                    )

            self.sensor_controller.subscribe_waist_rgbd_depth_camera_info(
                waist_rgbd_depth_camera_info_callback
            )
            self.subscriptions["waist_rgbd_depth_camera_info"] = True
            logging.info("✓ Waist RGBD depth camera info subscribed")

    # === Trinocular Camera Subscribe/Unsubscribe Methods ===
    def toggle_trinocular_image_subscription(self):
        """Toggle trinocular camera image subscription"""
        if self.subscriptions["trinocular_image"]:
            self.sensor_controller.unsubscribe_trinocular_image()
            self.subscriptions["trinocular_image"] = False
            logging.info("✓ Trinocular camera image unsubscribed")
        else:

            def trinocular_image_callback(frame):
                global trinocular_image_counter
                trinocular_image_counter += 1
                if trinocular_image_counter % 15 == 0:
                    logging.info(
                        f"Trinocular Camera Frame received (count: {trinocular_image_counter})"
                    )

            self.sensor_controller.subscribe_trinocular_image(trinocular_image_callback)
            self.subscriptions["trinocular_image"] = True
            logging.info("✓ Trinocular camera image subscribed")

    def show_status(self):
        """Display current sensor status"""
        logging.info("\n" + "=" * 80)
        logging.info("MAGICBOT GEN1 SENSOR STATUS")
        logging.info("=" * 80)
        logging.info(
            f"LiDAR:                         {'OPEN' if self.sensors_state['lidar'] else 'CLOSED'}"
        )
        logging.info(
            f"Head RGBD Camera:              {'OPEN' if self.sensors_state['head_rgbd_camera'] else 'CLOSED'}"
        )
        logging.info(
            f"Waist RGBD Camera:             {'OPEN' if self.sensors_state['waist_rgbd_camera'] else 'CLOSED'}"
        )
        logging.info(
            f"Trinocular Camera:             {'OPEN' if self.sensors_state['trinocular_camera'] else 'CLOSED'}"
        )
        logging.info("\nLIDAR SUBSCRIPTIONS:")
        logging.info(
            f"  LiDAR IMU:                   {'✓ SUBSCRIBED' if self.subscriptions['lidar_imu'] else '✗ UNSUBSCRIBED'}"
        )
        logging.info(
            f"  LiDAR Point Cloud:           {'✓ SUBSCRIBED' if self.subscriptions['lidar_point_cloud'] else '✗ UNSUBSCRIBED'}"
        )
        logging.info("\nHEAD RGBD SUBSCRIPTIONS:")
        logging.info(
            f"  Color Image:                 {'✓ SUBSCRIBED' if self.subscriptions['head_rgbd_color_image'] else '✗ UNSUBSCRIBED'}"
        )
        logging.info(
            f"  Color Camera Info:           {'✓ SUBSCRIBED' if self.subscriptions['head_rgbd_color_camera_info'] else '✗ UNSUBSCRIBED'}"
        )
        logging.info(
            f"  Depth Image:                 {'✓ SUBSCRIBED' if self.subscriptions['head_rgbd_depth_image'] else '✗ UNSUBSCRIBED'}"
        )
        logging.info(
            f"  Depth Camera Info:           {'✓ SUBSCRIBED' if self.subscriptions['head_rgbd_depth_camera_info'] else '✗ UNSUBSCRIBED'}"
        )
        logging.info("\nWAIST RGBD SUBSCRIPTIONS:")
        logging.info(
            f"  Color Image:                 {'✓ SUBSCRIBED' if self.subscriptions['waist_rgbd_color_image'] else '✗ UNSUBSCRIBED'}"
        )
        logging.info(
            f"  Color Camera Info:           {'✓ SUBSCRIBED' if self.subscriptions['waist_rgbd_color_camera_info'] else '✗ UNSUBSCRIBED'}"
        )
        logging.info(
            f"  Depth Image:                 {'✓ SUBSCRIBED' if self.subscriptions['waist_rgbd_depth_image'] else '✗ UNSUBSCRIBED'}"
        )
        logging.info(
            f"  Depth Camera Info:           {'✓ SUBSCRIBED' if self.subscriptions['waist_rgbd_depth_camera_info'] else '✗ UNSUBSCRIBED'}"
        )
        logging.info("\nTRINOCULAR CAMERA SUBSCRIPTIONS:")
        logging.info(
            f"  Trinocular Image:            {'✓ SUBSCRIBED' if self.subscriptions['trinocular_image'] else '✗ UNSUBSCRIBED'}"
        )
        logging.info("=" * 80 + "\n")


def print_menu():
    """Print interactive menu"""
    logging.info("\n" + "=" * 80)
    logging.info("MAGICBOT GEN1 SENSOR CONTROL MENU")
    logging.info("=" * 80)
    logging.info("Sensor Open/Close:")
    logging.info("  1 - Open LiDAR                     2 - Close LiDAR")
    logging.info("  3 - Open Head RGBD Camera          4 - Close Head RGBD Camera")
    logging.info("  5 - Open Waist RGBD Camera         6 - Close Waist RGBD Camera")
    logging.info("  7 - Open Trinocular Camera         8 - Close Trinocular Camera")
    logging.info("\nLiDAR Subscriptions:")
    logging.info("  i - Toggle LiDAR IMU               p - Toggle LiDAR Point Cloud")
    logging.info("\nHead RGBD Camera Subscriptions:")
    logging.info(
        "  c - Toggle Head Color Image        C - Toggle Head Color Camera Info"
    )
    logging.info(
        "  d - Toggle Head Depth Image        D - Toggle Head Depth Camera Info"
    )
    logging.info("\nWaist RGBD Camera Subscriptions:")
    logging.info(
        "  w - Toggle Waist Color Image       W - Toggle Waist Color Camera Info"
    )
    logging.info(
        "  e - Toggle Waist Depth Image       E - Toggle Waist Depth Camera Info"
    )
    logging.info("\nTrinocular Camera Subscriptions:")
    logging.info("  t - Toggle Trinocular Image")
    logging.info("\nCommands:")
    logging.info(
        "  s - Show Status                    ESC - Quit              ? - Help"
    )
    logging.info("=" * 80)


def main():
    """Main function"""
    logging.info("\n" + "=" * 80)
    logging.info("MagicBot Gen1 SDK Sensor Interactive Example")
    logging.info("=" * 80 + "\n")

    local_ip = "192.168.55.10"
    robot = magicbot.MagicRobot()

    if not robot.initialize(local_ip):
        logging.error("Robot initialization failed")
        return

    status = robot.connect()
    if status.code != ErrorCode.OK:
        logging.error(f"Robot connection failed: {status.message}")
        robot.shutdown()
        return

    logging.info("✓ Robot connected successfully\n")

    sensor_controller = robot.get_sensor_controller()

    # Initialize sensor controller
    if not sensor_controller.initialize():
        logging.error("Sensor controller initialization failed")
        robot.disconnect()
        robot.shutdown()
        return

    logging.info("✓ Sensor controller initialized successfully\n")

    sensor_manager = SensorManager(sensor_controller)

    print_menu()

    try:
        while True:
            choice = input("\nEnter your choice: ").strip()

            if choice == "\x1b":  # ESC key
                logging.info("ESC key pressed, exiting program...")
                break

            # Sensor open/close control
            if choice == "1":
                sensor_manager.open_lidar()
            elif choice == "2":
                sensor_manager.close_lidar()
            elif choice == "3":
                sensor_manager.open_head_rgbd_camera()
            elif choice == "4":
                sensor_manager.close_head_rgbd_camera()
            elif choice == "5":
                sensor_manager.open_waist_rgbd_camera()
            elif choice == "6":
                sensor_manager.close_waist_rgbd_camera()
            elif choice == "7":
                sensor_manager.open_trinocular_camera()
            elif choice == "8":
                sensor_manager.close_trinocular_camera()

            # LiDAR subscriptions
            elif choice == "i":
                sensor_manager.toggle_lidar_imu_subscription()
            elif choice == "p":
                sensor_manager.toggle_lidar_point_cloud_subscription()

            # Head RGBD subscriptions
            elif choice == "c":
                sensor_manager.toggle_head_rgbd_color_image_subscription()
            elif choice == "C":
                sensor_manager.toggle_head_rgbd_color_camera_info_subscription()
            elif choice == "d":
                sensor_manager.toggle_head_rgbd_depth_image_subscription()
            elif choice == "D":
                sensor_manager.toggle_head_rgbd_depth_camera_info_subscription()

            # Waist RGBD subscriptions
            elif choice == "w":
                sensor_manager.toggle_waist_rgbd_color_image_subscription()
            elif choice == "W":
                sensor_manager.toggle_waist_rgbd_color_camera_info_subscription()
            elif choice == "e":
                sensor_manager.toggle_waist_rgbd_depth_image_subscription()
            elif choice == "E":
                sensor_manager.toggle_waist_rgbd_depth_camera_info_subscription()

            # Trinocular camera subscriptions
            elif choice == "t":
                sensor_manager.toggle_trinocular_image_subscription()

            # Commands
            elif choice.lower() == "s":
                sensor_manager.show_status()
            elif choice == "?" or choice.lower() == "help":
                print_menu()
            else:
                logging.warning(f"Invalid choice: '{choice}'. Press '?' for help.")

    except KeyboardInterrupt:
        logging.info("\nReceived keyboard interrupt, shutting down...")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        import traceback

        traceback.print_exc()
    finally:
        # Cleanup: unsubscribe all and close all sensors
        logging.info("Cleaning up...")

        # Close all sensors
        if sensor_manager.sensors_state["lidar"]:
            sensor_manager.close_lidar()
        if sensor_manager.sensors_state["head_rgbd_camera"]:
            sensor_manager.close_head_rgbd_camera()
        if sensor_manager.sensors_state["waist_rgbd_camera"]:
            sensor_manager.close_waist_rgbd_camera()
        if sensor_manager.sensors_state["trinocular_camera"]:
            sensor_manager.close_trinocular_camera()

        # Allow time for cleanup
        time.sleep(1)

        sensor_controller.shutdown()
        logging.info("Sensor controller shutdown")

        robot.disconnect()
        logging.info("Robot disconnected")

        robot.shutdown()
        logging.info("Robot shutdown")


if __name__ == "__main__":
    main()
