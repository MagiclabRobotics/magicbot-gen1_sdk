#!/usr/bin/env python3
"""
Simple test case for RobotState data structure
Tests basic read/write operations for all fields
"""

import sys
import os

# Add the parent directory to the path to import magicbot_gen1_python
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

try:
    import magicbot_gen1_python as magicbot
except ImportError as e:
    print(f"Error importing magicbot_gen1_python: {e}")
    print("\n🔧 Troubleshooting steps:")
    print("1. Make sure the SDK is built:")
    print("   cd /path/to/magicbot_z1_sdk")
    print("   chmod +x build.sh")
    print("   ./build.sh")
    print("\n2. If the module is built but not installed, you may need to:")
    print("   - Add the build directory to PYTHONPATH")
    print("   - Or install the module to your Python environment")
    print("\n3. Check if the module exists in the build directory:")
    print("   find . -name '*magicbot*' -type f")
    print("\n4. If you're in a development environment, you might need to:")
    print("   export PYTHONPATH=/path/to/magicbot_z1_sdk/build:$PYTHONPATH")
    print(
        "\n📝 For now, this test will show the expected structure without running actual tests."
    )

    # Create a mock module for demonstration
    class MockMagicbot:
        class Fault:
            def __init__(self):
                self.error_code = 0
                self.error_message = ""

        class BmsData:
            def __init__(self):
                self.battery_percentage = 0.0
                self.battery_health = 0.0
                self.battery_state = 0
                self.power_supply_status = 0

        class RobotState:
            def __init__(self):
                self.faults = []
                self.bms_data = MockMagicbot.BmsData()

    magicbot = MockMagicbot()
    print("\n✅ Using mock module for demonstration purposes.")
    print("   (Replace with actual module when available)")


def test_fault():
    """Test Fault structure"""
    print("=== Testing Fault ===")

    fault = magicbot.Fault()

    # Test initial values
    print("   Testing initial values:")
    print(f"     error_code: {fault.error_code}")
    print(f"     error_message: '{fault.error_message}'")

    # Test setting values
    print("   Testing setting values:")
    fault.error_code = 1001
    fault.error_message = "Test error message"

    print(f"     Set error_code: {fault.error_code}")
    print(f"     Set error_message: '{fault.error_message}'")

    # Verify values
    assert fault.error_code == 1001
    assert fault.error_message == "Test error message"

    print("   ✓ Fault test passed")
    return True


def test_bms_data():
    """Test BmsData structure"""
    print("\n=== Testing BmsData ===")

    bms_data = magicbot.BmsData()

    # Test initial values
    print("   Testing initial values:")
    print(f"     battery_percentage: {bms_data.battery_percentage}")
    print(f"     battery_health: {bms_data.battery_health}")
    print(f"     battery_state: {bms_data.battery_state}")
    print(f"     power_supply_status: {bms_data.power_supply_status}")

    # Test setting values
    print("   Testing setting values:")
    bms_data.battery_percentage = 85.5
    bms_data.battery_health = 95.2
    bms_data.battery_state = magicbot.BatteryState.GOOD
    bms_data.power_supply_status = magicbot.PowerSupplyStatus.DISCHARGING

    print(f"     Set battery_percentage: {bms_data.battery_percentage}")
    print(f"     Set battery_health: {bms_data.battery_health}")
    print(f"     Set battery_state: {bms_data.battery_state}")
    print(f"     Set power_supply_status: {bms_data.power_supply_status}")

    # Verify values
    assert 85.5 - 1e-6 < bms_data.battery_percentage < 85.5 + 1e-6
    assert 95.2 - 1e-3 < bms_data.battery_health < 95.2 + 1e-3
    assert bms_data.battery_state == magicbot.BatteryState.GOOD
    assert bms_data.power_supply_status == magicbot.PowerSupplyStatus.DISCHARGING

    print("   ✓ BmsData test passed")
    return True


def test_robot_state():
    """Test RobotState structure"""
    print("\n=== Testing RobotState ===")

    robot_state = magicbot.RobotState()

    # Test initial values
    print("   Testing initial values:")
    print(f"     faults count: {len(robot_state.faults)}")
    print(
        f"     bms_data battery_percentage: {robot_state.bms_data.battery_percentage}"
    )

    # Test adding faults
    print("   Testing adding faults:")
    fault1 = magicbot.Fault()
    fault1.error_code = 1001
    fault1.error_message = "First test error"
    robot_state.faults.append(fault1)

    fault2 = magicbot.Fault()
    fault2.error_code = 1002
    fault2.error_message = "Second test error"
    robot_state.faults.append(fault2)

    print(f"     Added {len(robot_state.faults)} faults")
    assert len(robot_state.faults) == 2

    # Test setting BMS data
    print("   Testing setting BMS data:")
    robot_state.bms_data.battery_percentage = 75.0
    robot_state.bms_data.battery_health = 90.0
    robot_state.bms_data.battery_state = magicbot.BatteryState.GOOD
    robot_state.bms_data.power_supply_status = magicbot.PowerSupplyStatus.CHARGING

    print(f"     Set battery_percentage: {robot_state.bms_data.battery_percentage}")
    print(f"     Set battery_health: {robot_state.bms_data.battery_health}")
    print(f"     Set battery_state: {robot_state.bms_data.battery_state}")
    print(f"     Set power_supply_status: {robot_state.bms_data.power_supply_status}")

    # Verify values
    assert len(robot_state.faults) == 2
    assert robot_state.faults[0].error_code == 1001
    assert robot_state.faults[0].error_message == "First test error"
    assert robot_state.faults[1].error_code == 1002
    assert robot_state.faults[1].error_message == "Second test error"

    assert 75.0 - 1e-6 < robot_state.bms_data.battery_percentage < 75.0 + 1e-6
    assert 90.0 - 1e-6 < robot_state.bms_data.battery_health < 90.0 + 1e-6
    assert robot_state.bms_data.battery_state == magicbot.BatteryState.GOOD
    assert (
        robot_state.bms_data.power_supply_status == magicbot.PowerSupplyStatus.CHARGING
    )

    print("   ✓ RobotState test passed")
    return True


def test_robot_state_comprehensive():
    """Test comprehensive RobotState"""
    print("\n=== Testing RobotState Comprehensive ===")

    robot_state = magicbot.RobotState()

    # Test multiple faults
    print("   Testing multiple faults:")
    fault_codes = [1001, 1002, 1003, 1004]
    fault_messages = ["Error 1", "Error 2", "Error 3", "Error 4"]

    for code, message in zip(fault_codes, fault_messages):
        fault = magicbot.Fault()
        fault.error_code = code
        fault.error_message = message
        robot_state.faults.append(fault)
        print(f"     Added fault: code={code}, message='{message}'")

    print(f"     Total faults: {len(robot_state.faults)}")
    assert len(robot_state.faults) == 4

    # Test BMS data with different states
    print("   Testing BMS data with different states:")
    robot_state.bms_data.battery_percentage = 50.0
    robot_state.bms_data.battery_health = 80.0
    robot_state.bms_data.battery_state = magicbot.BatteryState.OVERHEAT
    robot_state.bms_data.power_supply_status = magicbot.PowerSupplyStatus.NOTCHARGING

    print(
        f"     Battery: {robot_state.bms_data.battery_percentage}%, health: {robot_state.bms_data.battery_health}"
    )
    print(
        f"     State: {robot_state.bms_data.battery_state}, Power status: {robot_state.bms_data.power_supply_status}"
    )

    # Verify comprehensive values
    for i, fault in enumerate(robot_state.faults):
        assert fault.error_code == fault_codes[i]
        assert fault.error_message == fault_messages[i]

    assert robot_state.bms_data.battery_percentage == 50.0
    assert robot_state.bms_data.battery_health == 80.0
    assert robot_state.bms_data.battery_state == magicbot.BatteryState.OVERHEAT
    assert (
        robot_state.bms_data.power_supply_status
        == magicbot.PowerSupplyStatus.NOTCHARGING
    )

    print("   ✓ Comprehensive test passed")
    return True


def main():
    """Main test function"""
    try:
        print("Starting RobotState binding tests...")
        print("=" * 50)

        test_fault()
        test_bms_data()
        test_robot_state()
        test_robot_state_comprehensive()

        print("\n" + "=" * 50)
        print("🎉 All RobotState binding tests completed successfully!")
        print("\nSummary:")
        print("  ✓ Fault - error_code, error_message")
        print(
            "  ✓ BmsData - battery_percentage, battery_health, battery_state, power_supply_status"
        )
        print("  ✓ RobotState - faults array, bms_data")
        print("  ✓ Comprehensive robot state with multiple faults and BMS data")

        return 0

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
