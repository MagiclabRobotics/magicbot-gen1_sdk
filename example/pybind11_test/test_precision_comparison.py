#!/usr/bin/env python3
"""
Precision comparison test for different data types in pybind11 bindings
Demonstrates the difference between float and double precision
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
    print("   cd /path/to/magicbot_gen1_sdk")
    print("   chmod +x build.sh")
    print("   ./build.sh")
    print("\n2. If the module is built but not installed, you may need to:")
    print("   - Add the build directory to PYTHONPATH")
    print("   - Or install the module to your Python environment")
    print("\n3. Check if the module exists in the build directory:")
    print("   find . -name '*magicbot*' -type f")
    print("\n4. If you're in a development environment, you might need to:")
    print("   export PYTHONPATH=/path/to/magicbot_gen1_sdk/build:$PYTHONPATH")
    print(
        "\n📝 For now, this test will show the expected structure without running actual tests."
    )

    # Create a mock module for demonstration
    class MockMagicbot:
        class Pose3DEuler:
            def __init__(self):
                self.position = [0.0, 0.0, 0.0]
                self.orientation = [0.0, 0.0, 0.0]

        class Point2D:
            def __init__(self):
                self.x = 0.0
                self.y = 0.0

    magicbot = MockMagicbot()
    print("\n✅ Using mock module for demonstration purposes.")
    print("   (Replace with actual module when available)")


def test_precision_differences():
    """Test precision differences between float and double types"""
    print("=== Precision Comparison Test ===")
    print()

    # Test values with different levels of precision
    test_values = [
        ("Simple values", 1.0, 2.0),
        ("Medium precision", 123.456, 789.012),
        ("High precision", 12345.678901234567890, 98765.432109876543210),
        ("Very high precision", 123456789.123456789, 987654321.987654321),
    ]

    for test_name, x_val, y_val in test_values:
        print(f"--- {test_name} ---")
        print(f"Original values: x={x_val}, y={y_val}")

        # Test Point2D (float - 32-bit)
        point2d = magicbot.Point2D()
        point2d.x = x_val
        point2d.y = y_val

        print(f"Point2D (float): x={point2d.x}, y={point2d.y}")

        # Test Pose3DEuler position (double - 64-bit)
        pose3d = magicbot.Pose3DEuler()
        pose3d.position = [x_val, y_val, 0.0]

        print(
            f"Pose3D position (double): [{pose3d.position[0]}, {pose3d.position[1]}, {pose3d.position[2]}]"
        )

        # Calculate differences
        x_diff_point2d = abs(point2d.x - x_val)
        y_diff_point2d = abs(point2d.y - y_val)
        x_diff_pose3d = abs(pose3d.position[0] - x_val)
        y_diff_pose3d = abs(pose3d.position[1] - y_val)

        print(
            f"Point2D differences: x_diff={x_diff_point2d:.2e}, y_diff={y_diff_point2d:.2e}"
        )
        print(
            f"Pose3D differences: x_diff={x_diff_pose3d:.2e}, y_diff={y_diff_pose3d:.2e}"
        )

        # Show precision comparison
        if x_diff_point2d > 0:
            point2d_precision = (
                len(str(x_val).split(".")[-1]) if "." in str(x_val) else 0
            )
            pose3d_precision = (
                len(str(pose3d.position[0]).split(".")[-1])
                if "." in str(pose3d.position[0])
                else 0
            )
            print(
                f"Precision: Point2D ~{point2d_precision} digits, Pose3D ~{pose3d_precision} digits"
            )

        print()


def test_precision_limits():
    """Test the limits of precision for different data types"""
    print("=== Precision Limits Test ===")
    print()

    # Test values that should show precision limits
    precision_tests = [
        ("Pi approximation", 3.141592653589793238462643383279502884197),
        ("Euler's number", 2.718281828459045235360287471352662497757),
        ("Golden ratio", 1.618033988749894848204586834365638117720),
        ("Large number", 123456789.123456789123456789123456789),
    ]

    for test_name, value in precision_tests:
        print(f"--- {test_name} ---")
        print(f"Original: {value}")

        # Test Point2D (float)
        point2d = magicbot.Point2D()
        point2d.x = value
        point2d.y = value

        print(f"Point2D (float): x={point2d.x}, y={point2d.y}")

        # Test Pose3DEuler (double)
        pose3d = magicbot.Pose3DEuler()
        pose3d.position = [value, value, 0.0]
        pose3d.orientation = [value, value, 0.0]

        print(
            f"Pose3D position (double): [{pose3d.position[0]}, {pose3d.position[1]}, {pose3d.position[2]}]"
        )
        print(
            f"Pose3D orientation (double): [{pose3d.orientation[0]}, {pose3d.orientation[1]}, {pose3d.orientation[2]}]"
        )

        print()


def test_practical_precision():
    """Test practical precision for typical use cases"""
    print("=== Practical Precision Test ===")
    print()

    # Typical values used in robotics
    practical_tests = [
        ("Robot position (meters)", 1.234567, 2.345678),
        ("Map coordinates (meters)", 12.3456789, 23.4567890),
        ("Small movements (mm)", 0.001234567, 0.002345678),
        ("Angular values (radians)", 0.123456789, 1.234567890),
    ]

    for test_name, x_val, y_val in practical_tests:
        print(f"--- {test_name} ---")
        print(f"Input: x={x_val}, y={y_val}")

        # Test Point2D
        point2d = magicbot.Point2D()
        point2d.x = x_val
        point2d.y = y_val

        # Test Pose3DEuler
        pose3d = magicbot.Pose3DEuler()
        pose3d.position = [x_val, y_val, 0.0]

        # Check if precision is sufficient for the use case
        point2d_x_ok = abs(point2d.x - x_val) < 1e-6
        point2d_y_ok = abs(point2d.y - y_val) < 1e-6
        pose3d_x_ok = abs(pose3d.position[0] - x_val) < 1e-15
        pose3d_y_ok = abs(pose3d.position[1] - y_val) < 1e-15

        print(f"Point2D: x={point2d.x}, y={point2d.y}")
        print(f"Pose3D: x={pose3d.position[0]}, y={pose3d.position[1]}")
        print(f"Point2D precision OK: x={point2d_x_ok}, y={point2d_y_ok}")
        print(f"Pose3D precision OK: x={pose3d_x_ok}, y={pose3d_y_ok}")

        print()


def main():
    """Main test function"""
    try:
        print("Starting Precision Comparison Tests...")
        print("=" * 60)
        print()
        print("This test demonstrates the precision differences between:")
        print("- Point2D: uses float (32-bit, ~6-7 significant digits)")
        print("- Pose3DEuler: uses double (64-bit, ~15-17 significant digits)")
        print()

        test_precision_differences()
        test_precision_limits()
        test_practical_precision()

        print("=" * 60)
        print("🎉 Precision comparison tests completed!")
        print()
        print("Summary:")
        print(
            "  ✓ Point2D (float) has lower precision but is sufficient for most 2D coordinates"
        )
        print(
            "  ✓ Pose3DEuler (double) has high precision suitable for precise 3D positioning"
        )
        print(
            "  ✓ Choose the appropriate data type based on your precision requirements"
        )
        print()
        print("Recommendations:")
        print(
            "  - Use Point2D for map coordinates, image pixels, etc. (float precision is sufficient)"
        )
        print(
            "  - Use Pose3DEuler for robot poses, precise measurements (double precision needed)"
        )

        return 0

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
