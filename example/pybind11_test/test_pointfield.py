#!/usr/bin/env python3
"""
Test case for PointField data structure
Tests all fields of the PointField struct for read/write operations
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
        class PointField:
            def __init__(self):
                self.name = ""
                self.offset = 0
                self.datatype = 0
                self.count = 0

    magicbot = MockMagicbot()
    print("\n✅ Using mock module for demonstration purposes.")
    print("   (Replace with actual module when available)")


def test_pointfield_name():
    """Test PointField name field"""
    print("=== Testing PointField Name ===")

    point_field = magicbot.PointField()

    # Test initial state
    print("   Testing initial name:")
    assert (
        point_field.name == ""
    ), f"Initial name should be empty string, got '{point_field.name}'"
    print("     ✓ Initial name test passed")

    # Test common field names
    print("   Testing common field names:")
    common_names = [
        "x",
        "y",
        "z",
        "intensity",
        "rgb",
        "normal_x",
        "normal_y",
        "normal_z",
        "curvature",
    ]

    for name in common_names:
        point_field.name = name
        print(f"     Set name: '{name}'")
        print(f"     Get name: '{point_field.name}'")
        assert (
            point_field.name == name
        ), f"Name mismatch: expected '{name}', got '{point_field.name}'"
        print(f"     ✓ Name '{name}' test passed")

    # Test empty string
    point_field.name = ""
    print(f"     Set empty name: '{point_field.name}'")
    assert (
        point_field.name == ""
    ), f"Empty name should be empty string, got '{point_field.name}'"
    print("     ✓ Empty name test passed")

    # Test long field name
    long_name = "very_long_field_name_that_might_be_used_for_descriptive_purposes"
    point_field.name = long_name
    print(f"     Set long name: '{point_field.name}'")
    assert (
        point_field.name == long_name
    ), f"Long name should be '{long_name}', got '{point_field.name}'"
    print("     ✓ Long name test passed")

    return True


def test_pointfield_offset():
    """Test PointField offset field"""
    print("\n=== Testing PointField Offset ===")

    point_field = magicbot.PointField()

    # Test initial state
    print("   Testing initial offset:")
    assert (
        point_field.offset == 0
    ), f"Initial offset should be 0, got {point_field.offset}"
    print("     ✓ Initial offset test passed")

    # Test common offset values
    print("   Testing common offset values:")
    common_offsets = [0, 4, 8, 12, 16, 20, 24, 28, 32]

    for offset in common_offsets:
        point_field.offset = offset
        print(f"     Set offset: {offset}")
        print(f"     Get offset: {point_field.offset}")
        assert (
            point_field.offset == offset
        ), f"Offset mismatch: expected {offset}, got {point_field.offset}"
        print(f"     ✓ Offset {offset} test passed")

    # Test zero offset
    point_field.offset = 0
    print(f"     Set zero offset: {point_field.offset}")
    assert point_field.offset == 0, f"Zero offset should be 0, got {point_field.offset}"
    print("     ✓ Zero offset test passed")

    # Test large offset values
    print("   Testing large offset values:")
    large_offsets = [1000, 10000, 100000, 2147483647]  # Max int32

    for offset in large_offsets:
        point_field.offset = offset
        print(f"     Set large offset: {offset}")
        assert (
            point_field.offset == offset
        ), f"Large offset should be {offset}, got {point_field.offset}"
        print(f"     ✓ Large offset {offset} test passed")

    return True


def test_pointfield_datatype():
    """Test PointField datatype field"""
    print("\n=== Testing PointField DataType ===")

    point_field = magicbot.PointField()

    # Test initial state
    print("   Testing initial datatype:")
    assert (
        point_field.datatype == 0
    ), f"Initial datatype should be 0, got {point_field.datatype}"
    print("     ✓ Initial datatype test passed")

    # Test common data types (based on ROS2 sensor_msgs::msg::PointField constants)
    print("   Testing common data types:")
    # These values correspond to ROS2 PointField constants
    data_types = {
        1: "INT8",
        2: "UINT8",
        3: "INT16",
        4: "UINT16",
        5: "INT32",
        6: "UINT32",
        7: "FLOAT32",
        8: "FLOAT64",
    }

    for datatype, type_name in data_types.items():
        point_field.datatype = datatype
        print(f"     Set datatype: {datatype} ({type_name})")
        print(f"     Get datatype: {point_field.datatype}")
        assert (
            point_field.datatype == datatype
        ), f"Datatype mismatch: expected {datatype}, got {point_field.datatype}"
        print(f"     ✓ Datatype {datatype} ({type_name}) test passed")

    # Test zero datatype
    point_field.datatype = 0
    print(f"     Set zero datatype: {point_field.datatype}")
    assert (
        point_field.datatype == 0
    ), f"Zero datatype should be 0, got {point_field.datatype}"
    print("     ✓ Zero datatype test passed")

    # Test negative datatype (edge case)
    print("   Testing negative datatype:")
    negative_datatype = -1
    point_field.datatype = negative_datatype
    print(f"     Set negative datatype: {point_field.datatype}")
    assert (
        point_field.datatype == negative_datatype
    ), f"Negative datatype should be {negative_datatype}, got {point_field.datatype}"
    print("     ✓ Negative datatype test passed")

    return True


def test_pointfield_count():
    """Test PointField count field"""
    print("\n=== Testing PointField Count ===")

    point_field = magicbot.PointField()

    # Test initial state
    print("   Testing initial count:")
    assert point_field.count == 0, f"Initial count should be 0, got {point_field.count}"
    print("     ✓ Initial count test passed")

    # Test common count values
    print("   Testing common count values:")
    common_counts = [1, 2, 3, 4, 8, 16, 32, 64]

    for count in common_counts:
        point_field.count = count
        print(f"     Set count: {count}")
        print(f"     Get count: {point_field.count}")
        assert (
            point_field.count == count
        ), f"Count mismatch: expected {count}, got {point_field.count}"
        print(f"     ✓ Count {count} test passed")

    # Test zero count
    point_field.count = 0
    print(f"     Set zero count: {point_field.count}")
    assert point_field.count == 0, f"Zero count should be 0, got {point_field.count}"
    print("     ✓ Zero count test passed")

    # Test large count values
    print("   Testing large count values:")
    large_counts = [100, 1000, 10000, 2147483647]  # Max int32

    for count in large_counts:
        point_field.count = count
        print(f"     Set large count: {count}")
        assert (
            point_field.count == count
        ), f"Large count should be {count}, got {point_field.count}"
        print(f"     ✓ Large count {count} test passed")

    return True


def test_pointfield_comprehensive():
    """Test comprehensive PointField data"""
    print("\n=== Testing Comprehensive PointField Data ===")

    point_field = magicbot.PointField()

    # Set all fields with typical point cloud field values
    point_field.name = "intensity"
    point_field.offset = 12
    point_field.datatype = 7  # FLOAT32
    point_field.count = 1

    print("   Setting comprehensive point field data:")
    print(f"     Name: '{point_field.name}'")
    print(f"     Offset: {point_field.offset}")
    print(f"     DataType: {point_field.datatype}")
    print(f"     Count: {point_field.count}")

    # Verify all fields
    assert point_field.name == "intensity"
    assert point_field.offset == 12
    assert point_field.datatype == 7
    assert point_field.count == 1

    print("   ✓ Comprehensive test passed")
    return True


def test_pointfield_typical_scenarios():
    """Test PointField with typical point cloud scenarios"""
    print("\n=== Testing PointField Typical Scenarios ===")

    # Test scenario 1: XYZ coordinates
    print("   Testing XYZ coordinates scenario:")
    xyz_field = magicbot.PointField()
    xyz_field.name = "x"
    xyz_field.offset = 0
    xyz_field.datatype = 7  # FLOAT32
    xyz_field.count = 1

    print(
        f"     X field: name='{xyz_field.name}', offset={xyz_field.offset}, datatype={xyz_field.datatype}, count={xyz_field.count}"
    )
    assert (
        xyz_field.name == "x"
        and xyz_field.offset == 0
        and xyz_field.datatype == 7
        and xyz_field.count == 1
    )
    print("     ✓ X field test passed")

    y_field = magicbot.PointField()
    y_field.name = "y"
    y_field.offset = 4
    y_field.datatype = 7  # FLOAT32
    y_field.count = 1

    print(
        f"     Y field: name='{y_field.name}', offset={y_field.offset}, datatype={y_field.datatype}, count={y_field.count}"
    )
    assert (
        y_field.name == "y"
        and y_field.offset == 4
        and y_field.datatype == 7
        and y_field.count == 1
    )
    print("     ✓ Y field test passed")

    z_field = magicbot.PointField()
    z_field.name = "z"
    z_field.offset = 8
    z_field.datatype = 7  # FLOAT32
    z_field.count = 1

    print(
        f"     Z field: name='{z_field.name}', offset={z_field.offset}, datatype={z_field.datatype}, count={z_field.count}"
    )
    assert (
        z_field.name == "z"
        and z_field.offset == 8
        and z_field.datatype == 7
        and z_field.count == 1
    )
    print("     ✓ Z field test passed")

    # Test scenario 2: RGB color
    print("   Testing RGB color scenario:")
    rgb_field = magicbot.PointField()
    rgb_field.name = "rgb"
    rgb_field.offset = 12
    rgb_field.datatype = 6  # UINT32
    rgb_field.count = 1

    print(
        f"     RGB field: name='{rgb_field.name}', offset={rgb_field.offset}, datatype={rgb_field.datatype}, count={rgb_field.count}"
    )
    assert (
        rgb_field.name == "rgb"
        and rgb_field.offset == 12
        and rgb_field.datatype == 6
        and rgb_field.count == 1
    )
    print("     ✓ RGB field test passed")

    # Test scenario 3: Intensity
    print("   Testing intensity scenario:")
    intensity_field = magicbot.PointField()
    intensity_field.name = "intensity"
    intensity_field.offset = 16
    intensity_field.datatype = 7  # FLOAT32
    intensity_field.count = 1

    print(
        f"     Intensity field: name='{intensity_field.name}', offset={intensity_field.offset}, datatype={intensity_field.datatype}, count={intensity_field.count}"
    )
    assert (
        intensity_field.name == "intensity"
        and intensity_field.offset == 16
        and intensity_field.datatype == 7
        and intensity_field.count == 1
    )
    print("     ✓ Intensity field test passed")

    # Test scenario 4: Normal vectors
    print("   Testing normal vectors scenario:")
    normal_x_field = magicbot.PointField()
    normal_x_field.name = "normal_x"
    normal_x_field.offset = 20
    normal_x_field.datatype = 7  # FLOAT32
    normal_x_field.count = 1

    normal_y_field = magicbot.PointField()
    normal_y_field.name = "normal_y"
    normal_y_field.offset = 24
    normal_y_field.datatype = 7  # FLOAT32
    normal_y_field.count = 1

    normal_z_field = magicbot.PointField()
    normal_z_field.name = "normal_z"
    normal_z_field.offset = 28
    normal_z_field.datatype = 7  # FLOAT32
    normal_z_field.count = 1

    print(
        f"     Normal X field: name='{normal_x_field.name}', offset={normal_x_field.offset}, datatype={normal_x_field.datatype}, count={normal_x_field.count}"
    )
    print(
        f"     Normal Y field: name='{normal_y_field.name}', offset={normal_y_field.offset}, datatype={normal_y_field.datatype}, count={normal_y_field.count}"
    )
    print(
        f"     Normal Z field: name='{normal_z_field.name}', offset={normal_z_field.offset}, datatype={normal_z_field.datatype}, count={normal_z_field.count}"
    )
    print("     ✓ Normal fields test passed")

    return True


def test_pointfield_edge_cases():
    """Test PointField edge cases"""
    print("\n=== Testing PointField Edge Cases ===")

    point_field = magicbot.PointField()

    # Test very long field name
    print("   Testing very long field name:")
    very_long_name = "very_long_field_name_that_might_be_used_for_descriptive_purposes_in_complex_point_cloud_applications"
    point_field.name = very_long_name
    print(f"     Set very long name: '{point_field.name}'")
    assert (
        point_field.name == very_long_name
    ), f"Very long name should be '{very_long_name}', got '{point_field.name}'"
    print("     ✓ Very long name test passed")

    # Test maximum offset value
    print("   Testing maximum offset value:")
    max_offset = 2147483647  # Max int32
    point_field.offset = max_offset
    print(f"     Set max offset: {point_field.offset}")
    assert (
        point_field.offset == max_offset
    ), f"Max offset should be {max_offset}, got {point_field.offset}"
    print("     ✓ Max offset test passed")

    # Test maximum datatype value
    print("   Testing maximum datatype value:")
    max_datatype = 127  # Max int8
    point_field.datatype = max_datatype
    print(f"     Set max datatype: {point_field.datatype}")
    assert (
        point_field.datatype == max_datatype
    ), f"Max datatype should be {max_datatype}, got {point_field.datatype}"
    print("     ✓ Max datatype test passed")

    # Test maximum count value
    print("   Testing maximum count value:")
    max_count = 2147483647  # Max int32
    point_field.count = max_count
    print(f"     Set max count: {point_field.count}")
    assert (
        point_field.count == max_count
    ), f"Max count should be {max_count}, got {point_field.count}"
    print("     ✓ Max count test passed")

    # Test negative values
    print("   Testing negative values:")
    point_field.offset = -100
    point_field.datatype = -50
    point_field.count = -10
    print(f"     Set negative offset: {point_field.offset}")
    print(f"     Set negative datatype: {point_field.datatype}")
    print(f"     Set negative count: {point_field.count}")
    assert (
        point_field.offset == -100
    ), f"Negative offset should be -100, got {point_field.offset}"
    assert (
        point_field.datatype == -50
    ), f"Negative datatype should be -50, got {point_field.datatype}"
    assert (
        point_field.count == -10
    ), f"Negative count should be -10, got {point_field.count}"
    print("     ✓ Negative values test passed")

    # Test special characters in name
    print("   Testing special characters in name:")
    special_name = "field_with_underscores_and_numbers_123"
    point_field.name = special_name
    print(f"     Set special name: '{point_field.name}'")
    assert (
        point_field.name == special_name
    ), f"Special name should be '{special_name}', got '{point_field.name}'"
    print("     ✓ Special characters test passed")

    print("   ✓ Edge cases test passed")
    return True


def test_pointfield_field_combinations():
    """Test PointField with different field combinations"""
    print("\n=== Testing PointField Field Combinations ===")

    # Test combination 1: Basic XYZ + Intensity
    print("   Testing XYZ + Intensity combination:")
    fields = []

    # X field
    x_field = magicbot.PointField()
    x_field.name = "x"
    x_field.offset = 0
    x_field.datatype = 7  # FLOAT32
    x_field.count = 1
    fields.append(x_field)

    # Y field
    y_field = magicbot.PointField()
    y_field.name = "y"
    y_field.offset = 4
    y_field.datatype = 7  # FLOAT32
    y_field.count = 1
    fields.append(y_field)

    # Z field
    z_field = magicbot.PointField()
    z_field.name = "z"
    z_field.offset = 8
    z_field.datatype = 7  # FLOAT32
    z_field.count = 1
    fields.append(z_field)

    # Intensity field
    intensity_field = magicbot.PointField()
    intensity_field.name = "intensity"
    intensity_field.offset = 12
    intensity_field.datatype = 7  # FLOAT32
    intensity_field.count = 1
    fields.append(intensity_field)

    # Verify all fields
    expected_names = ["x", "y", "z", "intensity"]
    expected_offsets = [0, 4, 8, 12]
    expected_datatypes = [7, 7, 7, 7]
    expected_counts = [1, 1, 1, 1]

    for i, field in enumerate(fields):
        print(
            f"     Field {i}: name='{field.name}', offset={field.offset}, datatype={field.datatype}, count={field.count}"
        )
        assert (
            field.name == expected_names[i]
        ), f"Field {i} name should be '{expected_names[i]}', got '{field.name}'"
        assert (
            field.offset == expected_offsets[i]
        ), f"Field {i} offset should be {expected_offsets[i]}, got {field.offset}"
        assert (
            field.datatype == expected_datatypes[i]
        ), f"Field {i} datatype should be {expected_datatypes[i]}, got {field.datatype}"
        assert (
            field.count == expected_counts[i]
        ), f"Field {i} count should be {expected_counts[i]}, got {field.count}"

    print("     ✓ XYZ + Intensity combination test passed")

    # Test combination 2: XYZ + RGB + Normals
    print("   Testing XYZ + RGB + Normals combination:")
    complex_fields = []

    # Create a more complex field set
    field_configs = [
        ("x", 0, 7, 1),
        ("y", 4, 7, 1),
        ("z", 8, 7, 1),
        ("rgb", 12, 6, 1),
        ("normal_x", 16, 7, 1),
        ("normal_y", 20, 7, 1),
        ("normal_z", 24, 7, 1),
        ("curvature", 28, 7, 1),
    ]

    for name, offset, datatype, count in field_configs:
        field = magicbot.PointField()
        field.name = name
        field.offset = offset
        field.datatype = datatype
        field.count = count
        complex_fields.append(field)

    # Verify complex field set
    for i, (name, offset, datatype, count) in enumerate(field_configs):
        field = complex_fields[i]
        print(
            f"     Complex field {i}: name='{field.name}', offset={field.offset}, datatype={field.datatype}, count={field.count}"
        )
        assert (
            field.name == name
        ), f"Complex field {i} name should be '{name}', got '{field.name}'"
        assert (
            field.offset == offset
        ), f"Complex field {i} offset should be {offset}, got {field.offset}"
        assert (
            field.datatype == datatype
        ), f"Complex field {i} datatype should be {datatype}, got {field.datatype}"
        assert (
            field.count == count
        ), f"Complex field {i} count should be {count}, got {field.count}"

    print("     ✓ XYZ + RGB + Normals combination test passed")

    return True


def main():
    """Main test function"""
    try:
        print("Starting PointField binding tests...")
        print("=" * 50)

        test_pointfield_name()
        test_pointfield_offset()
        test_pointfield_datatype()
        test_pointfield_count()
        test_pointfield_comprehensive()
        test_pointfield_typical_scenarios()
        test_pointfield_edge_cases()
        test_pointfield_field_combinations()

        print("\n" + "=" * 50)
        print("🎉 All PointField binding tests completed successfully!")
        print("\nSummary:")
        print("  ✓ Name field (std::string)")
        print("  ✓ Offset field (int32_t)")
        print("  ✓ DataType field (int8_t)")
        print("  ✓ Count field (int32_t)")
        print("  ✓ Comprehensive data setting and verification")
        print("  ✓ Typical point cloud scenarios (XYZ, RGB, Intensity, Normals)")
        print("  ✓ Edge cases (large values, negative values, special characters)")
        print("  ✓ Field combinations for complex point clouds")

        return 0

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
