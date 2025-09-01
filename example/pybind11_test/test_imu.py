#!/usr/bin/env python3

import sys
import magicbot_gen1_python as magicbot

def test_imu_basic_fields():
    """Test basic fields of Imu struct"""
    print("=== Testing Imu Basic Fields ===")
    
    imu = magicbot.Imu()
    
    # Test timestamp
    print("\n1. Testing timestamp field:")
    test_timestamp = 1234567890123456789
    imu.timestamp = test_timestamp
    print(f"   Set timestamp: {test_timestamp}")
    print(f"   Get timestamp: {imu.timestamp}")
    assert imu.timestamp == test_timestamp, f"Timestamp mismatch: expected {test_timestamp}, got {imu.timestamp}"
    print("   ✓ Timestamp test passed")
    
    # Test temperature
    print("\n2. Testing temperature field:")
    test_temperature = 25.5
    imu.temperature = test_temperature
    print(f"   Set temperature: {test_temperature}")
    print(f"   Get temperature: {imu.temperature}")
    assert abs(imu.temperature - test_temperature) < 1e-6, f"Temperature mismatch: expected {test_temperature}, got {imu.temperature}"
    print("   ✓ Temperature test passed")
    
    return True

def test_imu_orientation():
    """Test orientation quaternion field"""
    print("\n=== Testing Imu Orientation (Quaternion) ===")
    
    imu = magicbot.Imu()
    
    # Test quaternion (4 elements: x, y, z, w)
    test_orientation = [0.0, 0.0, 0.0, 1.0]  # Identity quaternion
    print(f"   Setting orientation quaternion: {test_orientation}")
    
    # Set orientation
    imu.orientation = test_orientation
    print(f"   Orientation after set: {imu.orientation}")
    
    # Verify the values
    for i, expected in enumerate(test_orientation):
        assert abs(imu.orientation[i] - expected) < 1e-6, f"Orientation[{i}] mismatch: expected {expected}, got {imu.orientation[i]}"
    
    # Test different quaternion
    test_orientation2 = [0.707, 0.0, 0.0, 0.707]  # 90-degree rotation around X-axis
    print(f"   Setting new orientation: {test_orientation2}")
    imu.orientation = test_orientation2
    
    for i, expected in enumerate(test_orientation2):
        assert abs(imu.orientation[i] - expected) < 1e-6, f"Orientation[{i}] mismatch: expected {expected}, got {imu.orientation[i]}"
    
    print("   ✓ Orientation test passed")
    return True

def test_imu_angular_velocity():
    """Test angular velocity field"""
    print("\n=== Testing Imu Angular Velocity ===")
    
    imu = magicbot.Imu()
    
    # Test angular velocity (3 elements: x, y, z)
    test_angular_velocity = [0.1, 0.2, 0.3]  # rad/s
    print(f"   Setting angular velocity: {test_angular_velocity}")
    
    # Set angular velocity
    imu.angular_velocity = test_angular_velocity
    print(f"   Angular velocity after set: {imu.angular_velocity}")
    
    # Verify the values
    for i, expected in enumerate(test_angular_velocity):
        assert abs(imu.angular_velocity[i] - expected) < 1e-6, f"Angular velocity[{i}] mismatch: expected {expected}, got {imu.angular_velocity[i]}"
    
    # Test different values
    test_angular_velocity2 = [-0.5, 1.0, -0.8]
    print(f"   Setting new angular velocity: {test_angular_velocity2}")
    imu.angular_velocity = test_angular_velocity2
    
    for i, expected in enumerate(test_angular_velocity2):
        assert abs(imu.angular_velocity[i] - expected) < 1e-6, f"Angular velocity[{i}] mismatch: expected {expected}, got {imu.angular_velocity[i]}"
    
    print("   ✓ Angular velocity test passed")
    return True

def test_imu_linear_acceleration():
    """Test linear acceleration field"""
    print("\n=== Testing Imu Linear Acceleration ===")
    
    imu = magicbot.Imu()
    
    # Test linear acceleration (3 elements: x, y, z)
    test_linear_acceleration = [0.0, 0.0, 9.81]  # m/s^2 (gravity)
    print(f"   Setting linear acceleration: {test_linear_acceleration}")
    
    # Set linear acceleration
    imu.linear_acceleration = test_linear_acceleration
    print(f"   Linear acceleration after set: {imu.linear_acceleration}")
    
    # Verify the values
    for i, expected in enumerate(test_linear_acceleration):
        assert abs(imu.linear_acceleration[i] - expected) < 1e-6, f"Linear acceleration[{i}] mismatch: expected {expected}, got {imu.linear_acceleration[i]}"
    
    # Test different values
    test_linear_acceleration2 = [2.5, -1.8, 8.2]
    print(f"   Setting new linear acceleration: {test_linear_acceleration2}")
    imu.linear_acceleration = test_linear_acceleration2
    
    for i, expected in enumerate(test_linear_acceleration2):
        assert abs(imu.linear_acceleration[i] - expected) < 1e-6, f"Linear acceleration[{i}] mismatch: expected {expected}, got {imu.linear_acceleration[i]}"
    
    print("   ✓ Linear acceleration test passed")
    return True


if __name__ == "__main__":
    test_imu_basic_fields()
    test_imu_orientation()
    test_imu_angular_velocity()
    test_imu_linear_acceleration()

def main():
    """Main test function"""
    try:
        print("Starting Imu binding tests...")
        
        test_imu_basic_fields()
        test_imu_orientation()
        test_imu_angular_velocity()
        test_imu_linear_acceleration()

        print("\n🎉 All Imu binding tests completed successfully!")
        print("\nSummary:")
        print("  ✓ Basic fields (timestamp, temperature)")
        print("  ✓ Orientation quaternion (4 elements)")
        print("  ✓ Angular velocity (3 elements)")
        print("  ✓ Linear acceleration (3 elements)")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())