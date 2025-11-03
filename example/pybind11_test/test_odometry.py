#!/usr/bin/env python3
"""
Test script for Odometry pybind11 bindings
"""

import sys
import magicbot_gen1_python as magicbot


def test_odometry_basic():
    """Test basic Odometry creation and attribute access"""
    print("=" * 60)
    print("Test 1: Basic Odometry Creation")
    print("=" * 60)

    # Create Odometry instance
    odom = magicbot.Odometry()

    # Test header
    odom.header.stamp = 123456789
    odom.header.frame_id = "odom"
    print(f"Header stamp: {odom.header.stamp}")
    print(f"Header frame_id: {odom.header.frame_id}")

    # Test child_frame_id
    odom.child_frame_id = "base_link"
    print(f"Child frame_id: {odom.child_frame_id}")

    print("✓ Basic creation test passed\n")


def test_odometry_position():
    """Test position property"""
    print("=" * 60)
    print("Test 2: Position Property")
    print("=" * 60)

    odom = magicbot.Odometry()

    # Set position using list
    odom.position = [1.0, 2.0, 3.0]
    print(f"Position (set from list): {odom.position}")
    print(f"  x: {odom.position[0]}")
    print(f"  y: {odom.position[1]}")
    print(f"  z: {odom.position[2]}")

    # Modify individual elements
    odom.position[0] = 10.0
    print(f"Position after modifying x: {odom.position}")

    print("✓ Position test passed\n")


def test_odometry_orientation():
    """Test orientation property"""
    print("=" * 60)
    print("Test 3: Orientation Property")
    print("=" * 60)

    odom = magicbot.Odometry()

    # Set orientation using list (roll, pitch, yaw)
    odom.orientation = [0.1, 0.2, 0.3]
    print(f"Orientation (set from list): {odom.orientation}")
    print(f"  roll:  {odom.orientation[0]}")
    print(f"  pitch: {odom.orientation[1]}")
    print(f"  yaw:   {odom.orientation[2]}")

    print("✓ Orientation test passed\n")


def test_odometry_velocities():
    """Test linear and angular velocity properties"""
    print("=" * 60)
    print("Test 4: Velocity Properties")
    print("=" * 60)

    odom = magicbot.Odometry()

    # Set linear velocity
    odom.linear_velocity = [0.5, 0.0, 0.0]
    print(f"Linear velocity: {odom.linear_velocity}")
    print(f"  vx: {odom.linear_velocity[0]}")
    print(f"  vy: {odom.linear_velocity[1]}")
    print(f"  vz: {odom.linear_velocity[2]}")

    # Set angular velocity
    odom.angular_velocity = [0.0, 0.0, 0.1]
    print(f"Angular velocity: {odom.angular_velocity}")
    print(f"  wx: {odom.angular_velocity[0]}")
    print(f"  wy: {odom.angular_velocity[1]}")
    print(f"  wz: {odom.angular_velocity[2]}")

    print("✓ Velocity test passed\n")


def test_odometry_complete():
    """Test complete Odometry data"""
    print("=" * 60)
    print("Test 5: Complete Odometry Data")
    print("=" * 60)

    odom = magicbot.Odometry()

    # Set all fields
    odom.header.stamp = 1234567890
    odom.header.frame_id = "odom"
    odom.child_frame_id = "base_link"
    odom.position = [1.5, 2.5, 0.0]
    odom.orientation = [0.0, 0.0, 1.57]  # 90 degrees yaw
    odom.linear_velocity = [0.3, 0.0, 0.0]
    odom.angular_velocity = [0.0, 0.0, 0.2]

    # Print complete odometry
    print("Complete Odometry:")
    print(f"  Header:")
    print(f"    stamp: {odom.header.stamp}")
    print(f"    frame_id: {odom.header.frame_id}")
    print(f"  Child frame: {odom.child_frame_id}")
    print(
        f"  Position: [{odom.position[0]:.2f}, {odom.position[1]:.2f}, {odom.position[2]:.2f}]"
    )
    print(
        f"  Orientation: [{odom.orientation[0]:.2f}, {odom.orientation[1]:.2f}, {odom.orientation[2]:.2f}]"
    )
    print(
        f"  Linear velocity: [{odom.linear_velocity[0]:.2f}, {odom.linear_velocity[1]:.2f}, {odom.linear_velocity[2]:.2f}]"
    )
    print(
        f"  Angular velocity: [{odom.angular_velocity[0]:.2f}, {odom.angular_velocity[1]:.2f}, {odom.angular_velocity[2]:.2f}]"
    )

    print("✓ Complete data test passed\n")


def test_odometry_iteration():
    """Test iteration over array properties"""
    print("=" * 60)
    print("Test 6: Array Iteration")
    print("=" * 60)

    odom = magicbot.Odometry()
    odom.position = [1.0, 2.0, 3.0]

    print("Iterating over position:")
    for i, val in enumerate(odom.position):
        print(f"  position[{i}] = {val}")

    print("✓ Iteration test passed\n")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Odometry Pybind11 Binding Tests")
    print("=" * 60 + "\n")

    try:
        test_odometry_basic()
        test_odometry_position()
        test_odometry_orientation()
        test_odometry_velocities()
        test_odometry_complete()
        test_odometry_iteration()

        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return 0

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
