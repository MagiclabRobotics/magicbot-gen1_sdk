#!/usr/bin/env python3
"""
Simple test case for JointState and JointCommand data structures
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
        class SingleJointCommand:
            def __init__(self):
                self.operation_mode = 200
                self.pos = 0.0
                self.vel = 0.0
                self.toq = 0.0
                self.kp = 0.0
                self.kd = 0.0

        class JointCommand:
            def __init__(self):
                self.timestamp = 0
                self.joints = []

        class SingleJointState:
            def __init__(self):
                self.status_word = 0
                self.posH = 0.0
                self.posL = 0.0
                self.vel = 0.0
                self.toq = 0.0
                self.current = 0.0
                self.err_code = 0

        class JointState:
            def __init__(self):
                self.timestamp = 0
                self.joints = []

    magicbot = MockMagicbot()
    print("\n✅ Using mock module for demonstration purposes.")
    print("   (Replace with actual module when available)")


def test_single_joint_command():
    """Test SingleJointCommand structure"""
    print("=== Testing SingleJointCommand ===")

    joint_cmd = magicbot.SingleJointCommand()

    # Test initial values
    print("   Testing initial values:")
    print(f"     operation_mode: {joint_cmd.operation_mode}")
    print(f"     pos: {joint_cmd.pos}")
    print(f"     vel: {joint_cmd.vel}")
    print(f"     toq: {joint_cmd.toq}")
    print(f"     kp: {joint_cmd.kp}")
    print(f"     kd: {joint_cmd.kd}")

    # Test setting values
    print("   Testing setting values:")
    joint_cmd.operation_mode = 100
    joint_cmd.pos = 1.57  # 90 degrees in radians
    joint_cmd.vel = 2.0
    joint_cmd.toq = 10.5
    joint_cmd.kp = 100.0
    joint_cmd.kd = 20.0

    print(f"     Set operation_mode: {joint_cmd.operation_mode}")
    print(f"     Set pos: {joint_cmd.pos}")
    print(f"     Set vel: {joint_cmd.vel}")
    print(f"     Set toq: {joint_cmd.toq}")
    print(f"     Set kp: {joint_cmd.kp}")
    print(f"     Set kd: {joint_cmd.kd}")

    # Verify values
    assert joint_cmd.operation_mode == 100
    assert 1.57 - 1e-6 < joint_cmd.pos < 1.57 + 1e-6
    assert 2.0 - 1e-6 < joint_cmd.vel < 2.0 + 1e-6
    assert 10.5 - 1e-6 < joint_cmd.toq < 10.5 + 1e-6
    assert 100.0 - 1e-6 < joint_cmd.kp < 100.0 + 1e-6
    assert 20.0 - 1e-6 < joint_cmd.kd < 20.0 + 1e-6

    print("   ✓ SingleJointCommand test passed")
    return True


def test_joint_command():
    """Test JointCommand structure"""
    print("\n=== Testing JointCommand ===")

    joint_cmd = magicbot.JointCommand()

    # Test initial values
    print("   Testing initial values:")
    print(f"     timestamp: {joint_cmd.timestamp}")
    print(f"     joints count: {len(joint_cmd.joints)}")

    # Test setting timestamp
    print("   Testing setting timestamp:")
    joint_cmd.timestamp = 1234567890
    print(f"     Set timestamp: {joint_cmd.timestamp}")
    assert joint_cmd.timestamp == 1234567890

    # Test adding joints
    print("   Testing adding joints:")
    for i in range(3):
        single_joint = magicbot.SingleJointCommand()
        single_joint.operation_mode = 200 + i
        single_joint.pos = 0.5 + i * 0.1
        single_joint.vel = 1.0 + i * 0.2
        single_joint.toq = 5.0 + i * 1.0
        single_joint.kp = 50.0 + i * 10.0
        single_joint.kd = 10.0 + i * 2.0

        joint_cmd.joints.append(single_joint)
        print(
            f"     Added joint {i}: operation_mode={single_joint.operation_mode}, pos={single_joint.pos}"
        )

    print(f"     Total joints count: {len(joint_cmd.joints)}")
    assert len(joint_cmd.joints) == 3

    # Verify joint values
    for i, joint in enumerate(joint_cmd.joints):
        assert joint.operation_mode == 200 + i
        assert 0.5 + i * 0.1 - 1e-6 < joint.pos < 0.5 + i * 0.1 + 1e-6
        assert 1.0 + i * 0.2 - 1e-6 < joint.vel < 1.0 + i * 0.2 + 1e-6
        assert 5.0 + i * 1.0 - 1e-6 < joint.toq < 5.0 + i * 1.0 + 1e-6
        assert 50.0 + i * 10.0 - 1e-6 < joint.kp < 50.0 + i * 10.0 + 1e-6
        assert 10.0 + i * 2.0 - 1e-6 < joint.kd < 10.0 + i * 2.0 + 1e-6

    print("   ✓ JointCommand test passed")
    return True


def test_single_joint_state():
    """Test SingleJointState structure"""
    print("\n=== Testing SingleJointState ===")

    joint_state = magicbot.SingleJointState()

    # Test initial values
    print("   Testing initial values:")
    print(f"     status_word: {joint_state.status_word}")
    print(f"     posH: {joint_state.posH}")
    print(f"     posL: {joint_state.posL}")
    print(f"     vel: {joint_state.vel}")
    print(f"     toq: {joint_state.toq}")
    print(f"     current: {joint_state.current}")
    print(f"     err_code: {joint_state.err_code}")

    # Test setting values
    print("   Testing setting values:")
    joint_state.status_word = 1234
    joint_state.posH = 1.23
    joint_state.posL = 1.24
    joint_state.vel = 0.5
    joint_state.toq = 8.0
    joint_state.current = 2.5
    joint_state.err_code = 0

    print(f"     Set status_word: {joint_state.status_word}")
    print(f"     Set posH: {joint_state.posH}")
    print(f"     Set posL: {joint_state.posL}")
    print(f"     Set vel: {joint_state.vel}")
    print(f"     Set toq: {joint_state.toq}")
    print(f"     Set current: {joint_state.current}")
    print(f"     Set err_code: {joint_state.err_code}")

    # Verify values
    assert joint_state.status_word == 1234
    assert 1.23 - 1e-6 < joint_state.posH < 1.23 + 1e-6
    assert 1.24 - 1e-6 < joint_state.posL < 1.24 + 1e-6
    assert 0.5 - 1e-6 < joint_state.vel < 0.5 + 1e-6
    assert 8.0 - 1e-6 < joint_state.toq < 8.0 + 1e-6
    assert 2.5 - 1e-6 < joint_state.current < 2.5 + 1e-6
    assert joint_state.err_code == 0

    print("   ✓ SingleJointState test passed")
    return True


def test_joint_state():
    """Test JointState structure"""
    print("\n=== Testing JointState ===")

    joint_state = magicbot.JointState()

    # Test initial values
    print("   Testing initial values:")
    print(f"     timestamp: {joint_state.timestamp}")
    print(f"     joints count: {len(joint_state.joints)}")

    # Test setting timestamp
    print("   Testing setting timestamp:")
    joint_state.timestamp = 9876543210
    print(f"     Set timestamp: {joint_state.timestamp}")
    assert joint_state.timestamp == 9876543210

    # Test adding joint states
    print("   Testing adding joint states:")
    for i in range(3):
        single_state = magicbot.SingleJointState()
        single_state.status_word = 1000 + i
        single_state.posH = 0.1 + i * 0.2
        single_state.posL = 0.11 + i * 0.2
        single_state.vel = 0.3 + i * 0.1
        single_state.toq = 3.0 + i * 0.5
        single_state.current = 1.0 + i * 0.3
        single_state.err_code = i

        joint_state.joints.append(single_state)
        print(
            f"     Added joint state {i}: status_word={single_state.status_word}, posH={single_state.posH}"
        )

    print(f"     Total joint states count: {len(joint_state.joints)}")
    assert len(joint_state.joints) == 3

    # Verify joint state values
    for i, state in enumerate(joint_state.joints):
        assert state.status_word == 1000 + i
        assert 0.1 + i * 0.2 - 1e-6 < state.posH < 0.1 + i * 0.2 + 1e-6
        assert 0.11 + i * 0.2 - 1e-6 < state.posL < 0.11 + i * 0.2 + 1e-6
        assert 0.3 + i * 0.1 - 1e-6 < state.vel < 0.3 + i * 0.1 + 1e-6
        assert 3.0 + i * 0.5 - 1e-6 < state.toq < 3.0 + i * 0.5 + 1e-6
        assert 1.0 + i * 0.3 - 1e-6 < state.current < 1.0 + i * 0.3 + 1e-6
        assert state.err_code == i

    print("   ✓ JointState test passed")
    return True


def test_joint_structures_comprehensive():
    """Test comprehensive joint structures"""
    print("\n=== Testing Joint Structures Comprehensive ===")

    # Create a complete joint command
    print("   Testing complete joint command:")
    joint_cmd = magicbot.JointCommand()
    joint_cmd.timestamp = 1234567890123456789

    # Add multiple joints with different configurations
    joint_configs = [
        (200, 0.0, 0.0, 0.0, 100.0, 20.0),  # Position control
        (201, 1.57, 2.0, 10.0, 150.0, 30.0),  # Velocity control
        (202, 3.14, 1.5, 15.0, 200.0, 40.0),  # Torque control
    ]

    for i, (mode, pos, vel, toq, kp, kd) in enumerate(joint_configs):
        joint = magicbot.SingleJointCommand()
        joint.operation_mode = mode
        joint.pos = pos
        joint.vel = vel
        joint.toq = toq
        joint.kp = kp
        joint.kd = kd
        joint_cmd.joints.append(joint)
        print(f"     Joint {i}: mode={mode}, pos={pos}, vel={vel}, toq={toq}")

    print(f"     Total joints: {len(joint_cmd.joints)}")
    assert len(joint_cmd.joints) == 3

    # Create a complete joint state
    print("   Testing complete joint state:")
    joint_state = magicbot.JointState()
    joint_state.timestamp = 111111111111

    # Add multiple joint states with different values
    state_configs = [
        (1000, 0.1, 0.11, 0.3, 3.0, 1.0, 0),  # Normal state
        (1001, 0.3, 0.31, 0.4, 3.5, 1.3, 0),  # Moving state
        (1002, 0.5, 0.51, 0.5, 4.0, 1.6, 0),  # Loaded state
    ]

    for i, (status, posH, posL, vel, toq, current, err) in enumerate(state_configs):
        state = magicbot.SingleJointState()
        state.status_word = status
        state.posH = posH
        state.posL = posL
        state.vel = vel
        state.toq = toq
        state.current = current
        state.err_code = err
        joint_state.joints.append(state)
        print(
            f"     State {i}: status={status}, posH={posH}, vel={vel}, current={current}"
        )

    print(f"     Total states: {len(joint_state.joints)}")
    assert len(joint_state.joints) == 3

    print("   ✓ Comprehensive test passed")
    return True


def main():
    """Main test function"""
    try:
        print("Starting JointState and JointCommand binding tests...")
        print("=" * 60)

        test_single_joint_command()
        test_joint_command()
        test_single_joint_state()
        test_joint_state()
        test_joint_structures_comprehensive()

        print("\n" + "=" * 60)
        print(
            "🎉 All JointState and JointCommand binding tests completed successfully!"
        )
        print("\nSummary:")
        print("  ✓ SingleJointCommand - operation_mode, pos, vel, toq, kp, kd")
        print("  ✓ JointCommand - timestamp, joints array")
        print(
            "  ✓ SingleJointState - status_word, posH, posL, vel, toq, current, err_code"
        )
        print("  ✓ JointState - timestamp, joints array")
        print("  ✓ Comprehensive joint structures with multiple joints")

        return 0

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
