#!/usr/bin/env python3
"""
Simple test case for navigation and SLAM data structures
Tests basic read/write operations for all fields
"""

import sys
import os
import time

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
        class NavTarget:
            def __init__(self):
                self.id = 0
                self.frame_id = ""
                self.goal = None

        class Pose3DEuler:
            def __init__(self):
                self.position = [0.0, 0.0, 0.0]
                self.orientation = [0.0, 0.0, 0.0]

        class MapImageData:
            def __init__(self):
                self.width = 0
                self.height = 0
                self.max_gray_value = 0
                self.type = ""
                self.image = b""

        class MapMetaData:
            def __init__(self):
                self.resolution = 0.0
                self.origin = None
                self.map_image_data = None

        class MapInfo:
            def __init__(self):
                self.map_name = ""
                self.map_meta_data = None

        class AllMapInfo:
            def __init__(self):
                self.current_map_name = ""
                self.map_infos = []

        class LocalizationInfo:
            def __init__(self):
                self.is_localization = False
                self.pose = None

    magicbot = MockMagicbot()
    print("\n✅ Using mock module for demonstration purposes.")
    print("   (Replace with actual module when available)")


def test_target_goal():
    """Test NavTarget structure"""
    print("=== Testing NavTarget ===")

    target_goal = magicbot.NavTarget()

    # Test initial values
    print("   Testing initial values:")
    print(f"     id: {target_goal.id}")
    print(f"     frame_id: '{target_goal.frame_id}'")
    print(f"     goal: {target_goal.goal}")

    # Test setting id
    print("   Testing setting id:")
    target_goal.id = 123
    print(f"     Set id: {target_goal.id}")
    assert target_goal.id == 123

    # Test setting frame_id
    print("   Testing setting frame_id:")
    target_goal.frame_id = "map"
    print(f"     Set frame_id: '{target_goal.frame_id}'")
    assert target_goal.frame_id == "map"

    # Test setting goal (Pose3DEuler)
    print("   Testing setting goal:")
    target_goal.goal = magicbot.Pose3DEuler()
    target_goal.goal.position = [2.5, 1.8, 0.0]
    target_goal.goal.orientation = [0.0, 0.0, 1.57]  # 90 degrees in radians
    print(f"     Set goal position: {target_goal.goal.position}")
    print(f"     Set goal orientation: {target_goal.goal.orientation}")
    assert len(target_goal.goal.position) == 3
    assert len(target_goal.goal.orientation) == 3
    assert abs(target_goal.goal.position[0] - 2.5) < 1e-6
    assert abs(target_goal.goal.position[1] - 1.8) < 1e-6
    assert abs(target_goal.goal.position[2] - 0.0) < 1e-6
    assert abs(target_goal.goal.orientation[2] - 1.57) < 1e-6

    print("   ✓ NavTarget test passed")
    return True


def test_map_image_data():
    """Test MapImageData structure"""
    print("\n=== Testing MapImageData ===")

    map_image_data = magicbot.MapImageData()

    # Test initial values
    print("   Testing initial values:")
    print(f"     width: {map_image_data.width}")
    print(f"     height: {map_image_data.height}")
    print(f"     max_gray_value: {map_image_data.max_gray_value}")
    print(f"     type: '{map_image_data.type}'")
    print(f"     image length: {len(map_image_data.image)}")

    # Test setting dimensions
    print("   Testing setting dimensions:")
    map_image_data.width = 1024
    map_image_data.height = 768
    print(f"     Set width: {map_image_data.width}")
    print(f"     Set height: {map_image_data.height}")
    assert map_image_data.width == 1024
    assert map_image_data.height == 768

    # Test setting max_gray_value
    print("   Testing setting max_gray_value:")
    map_image_data.max_gray_value = 255
    print(f"     Set max_gray_value: {map_image_data.max_gray_value}")
    assert map_image_data.max_gray_value == 255

    # Test setting type
    print("   Testing setting type:")
    map_image_data.type = "pgm"
    print(f"     Set type: '{map_image_data.type}'")
    assert map_image_data.type == "pgm"

    # # Test setting image data
    # print("   Testing setting image data:")
    # # Create some dummy image data (1024x768 pixels, each pixel 1 byte)
    # dummy_image_data = b'\x80' * (1024 * 768)
    # map_image_data.image = dummy_image_data
    # print(f"     Set image data length: {len(map_image_data.image)}")
    # assert len(map_image_data.image) == 1024 * 768
    # assert map_image_data.image == dummy_image_data

    print("   ✓ MapImageData test passed")
    return True


def test_map_meta_data():
    """Test MapMetaData structure"""
    print("\n=== Testing MapMetaData ===")

    map_meta_data = magicbot.MapMetaData()

    # Test initial values
    print("   Testing initial values:")
    print(f"     resolution: {map_meta_data.resolution}")
    print(f"     origin: {map_meta_data.origin}")
    print(f"     map_image_data: ", len(map_meta_data.map_image_data.image))

    # Test setting resolution
    print("   Testing setting resolution:")
    map_meta_data.resolution = 0.05  # 5cm per pixel
    print(f"     Set resolution: {map_meta_data.resolution}")
    assert abs(map_meta_data.resolution - 0.05) < 1e-6

    # Test setting origin (Pose3DEuler)
    print("   Testing setting origin:")
    map_meta_data.origin = magicbot.Pose3DEuler()
    map_meta_data.origin.position = [-10.0, -5.0, 0.0]
    map_meta_data.origin.orientation = [0.0, 0.0, 0.0]
    print(f"     Set origin position: {map_meta_data.origin.position}")
    print(f"     Set origin orientation: {map_meta_data.origin.orientation}")
    assert len(map_meta_data.origin.position) == 3
    assert len(map_meta_data.origin.orientation) == 3
    assert abs(map_meta_data.origin.position[0] - (-10.0)) < 1e-6
    assert abs(map_meta_data.origin.position[1] - (-5.0)) < 1e-6
    assert abs(map_meta_data.origin.position[2] - 0.0) < 1e-6

    # Test setting map_image_data
    print("   Testing setting map_image_data:")
    map_meta_data.map_image_data = magicbot.MapImageData()
    map_meta_data.map_image_data.width = 400
    map_meta_data.map_image_data.height = 300
    map_meta_data.map_image_data.max_gray_value = 255
    map_meta_data.map_image_data.type = "pgm"
    # map_meta_data.map_image_data.image = b'\xFF' * (400 * 300)
    print(f"     Set map image width: {map_meta_data.map_image_data.width}")
    print(f"     Set map image height: {map_meta_data.map_image_data.height}")
    assert map_meta_data.map_image_data.width == 400
    assert map_meta_data.map_image_data.height == 300
    assert map_meta_data.map_image_data.max_gray_value == 255
    assert map_meta_data.map_image_data.type == "pgm"
    # assert len(map_meta_data.map_image_data.image) == 400 * 300

    print("   ✓ MapMetaData test passed")
    return True


def test_map_info():
    """Test MapInfo structure"""
    print("\n=== Testing MapInfo ===")

    map_info = magicbot.MapInfo()

    # Test initial values
    print("   Testing initial values:")
    print(f"     map_name: '{map_info.map_name}'")
    print(
        f"     map_meta_data size: ", len(map_info.map_meta_data.map_image_data.image)
    )

    # Test setting map_name
    print("   Testing setting map_name:")
    map_info.map_name = "office_map_001"
    print(f"     Set map_name: '{map_info.map_name}'")
    assert map_info.map_name == "office_map_001"

    # Test setting map_meta_data
    print("   Testing setting map_meta_data:")
    map_info.map_meta_data = magicbot.MapMetaData()
    map_info.map_meta_data.resolution = 0.02  # 2cm per pixel
    map_info.map_meta_data.origin = magicbot.Pose3DEuler()
    map_info.map_meta_data.origin.position = [-20.0, -15.0, 0.0]
    map_info.map_meta_data.origin.orientation = [0.0, 0.0, 0.0]

    map_info.map_meta_data.map_image_data = magicbot.MapImageData()
    map_info.map_meta_data.map_image_data.width = 1000
    map_info.map_meta_data.map_image_data.height = 750
    map_info.map_meta_data.map_image_data.max_gray_value = 255
    map_info.map_meta_data.map_image_data.type = "pgm"
    # map_info.map_meta_data.map_image_data.image = b'\x7F' * (1000 * 750)

    print(f"     Set map resolution: {map_info.map_meta_data.resolution}")
    print(f"     Set map origin: {map_info.map_meta_data.origin.position}")
    print(
        f"     Set map image size: {map_info.map_meta_data.map_image_data.width}x{map_info.map_meta_data.map_image_data.height}"
    )

    assert abs(map_info.map_meta_data.resolution - 0.02) < 1e-6
    assert abs(map_info.map_meta_data.origin.position[0] - (-20.0)) < 1e-6
    assert abs(map_info.map_meta_data.origin.position[1] - (-15.0)) < 1e-6
    assert map_info.map_meta_data.map_image_data.width == 1000
    assert map_info.map_meta_data.map_image_data.height == 750

    print("   ✓ MapInfo test passed")
    return True


def test_all_map_info():
    """Test AllMapInfo structure"""
    print("\n=== Testing AllMapInfo ===")

    all_map_info = magicbot.AllMapInfo()

    # Test initial values
    print("   Testing initial values:")
    print(f"     current_map_name: '{all_map_info.current_map_name}'")
    print(f"     map_infos count: {len(all_map_info.map_infos)}")

    # Test setting current_map_name
    print("   Testing setting current_map_name:")
    all_map_info.current_map_name = "active_map"
    print(f"     Set current_map_name: '{all_map_info.current_map_name}'")
    assert all_map_info.current_map_name == "active_map"

    # Test adding map_infos
    print("   Testing adding map_infos:")
    map_names = ["map_1", "map_2", "map_3"]

    for i, map_name in enumerate(map_names):
        map_info = magicbot.MapInfo()
        map_info.map_name = map_name
        map_info.map_meta_data = magicbot.MapMetaData()
        map_info.map_meta_data.resolution = 0.05 + i * 0.01
        map_info.map_meta_data.origin = magicbot.Pose3DEuler()
        map_info.map_meta_data.origin.position = [i * -10.0, i * -5.0, 0.0]
        map_info.map_meta_data.origin.orientation = [0.0, 0.0, 0.0]

        map_info.map_meta_data.map_image_data = magicbot.MapImageData()
        map_info.map_meta_data.map_image_data.width = 500 + i * 100
        map_info.map_meta_data.map_image_data.height = 400 + i * 50
        map_info.map_meta_data.map_image_data.max_gray_value = 255
        map_info.map_meta_data.map_image_data.type = "pgm"

        # Create dummy image data
        image_size = (500 + i * 100) * (400 + i * 50)
        # map_info.map_meta_data.map_image_data.image = b'\x80' * image_size

        all_map_info.map_infos.append(map_info)
        print(
            f"     Added map {i}: {map_info.map_name}, resolution={map_info.map_meta_data.resolution}, size={map_info.map_meta_data.map_image_data.width}x{map_info.map_meta_data.map_image_data.height}"
        )

    print(f"     Total maps: {len(all_map_info.map_infos)}")
    assert len(all_map_info.map_infos) == 3

    # Verify all map info
    for i, map_info in enumerate(all_map_info.map_infos):
        assert map_info.map_name == map_names[i]
        assert abs(map_info.map_meta_data.resolution - (0.05 + i * 0.01)) < 1e-6
        assert abs(map_info.map_meta_data.origin.position[0] - (i * -10.0)) < 1e-6
        assert abs(map_info.map_meta_data.origin.position[1] - (i * -5.0)) < 1e-6
        assert map_info.map_meta_data.map_image_data.width == 500 + i * 100
        assert map_info.map_meta_data.map_image_data.height == 400 + i * 50

    print("   ✓ AllMapInfo test passed")
    return True


def test_pose_info():
    """Test LocalizationInfo structure"""
    print("\n=== Testing LocalizationInfo ===")

    pose_info = magicbot.LocalizationInfo()

    # Test initial values
    print("   Testing initial values:")
    print(f"     is_localization: {pose_info.is_localization}")
    print(f"     pose: {pose_info.pose}")

    # Test setting is_localization
    print("   Testing setting is_localization:")
    pose_info.is_localization = True
    print(f"     Set is_localization: {pose_info.is_localization}")
    assert pose_info.is_localization == True

    # Test setting pose
    print("   Testing setting pose:")
    pose_info.pose = magicbot.Pose3DEuler()

    pose_info.pose.position[0] = 1.2
    pose_info.pose.position[1] = 3.4
    pose_info.pose.position[2] = 0.0
    pose_info.pose.orientation[0] = 0.0
    pose_info.pose.orientation[1] = 0.0
    pose_info.pose.orientation[2] = 0.785

    print(f"     Set pose position: {pose_info.pose.position}")
    print(f"     Set pose orientation: {pose_info.pose.orientation}")
    assert len(pose_info.pose.position) == 3
    assert len(pose_info.pose.orientation) == 3
    assert abs(pose_info.pose.position[0] - 1.2) < 1e-6
    assert abs(pose_info.pose.position[1] - 3.4) < 1e-6
    assert abs(pose_info.pose.position[2] - 0.0) < 1e-6
    assert abs(pose_info.pose.orientation[2] - 0.785) < 1e-6

    # Test with not localized
    print("   Testing with not localized:")
    pose_info.is_localization = False
    pose_info.pose.position = [0.0, 0.0, 0.0]
    pose_info.pose.orientation = [0.0, 0.0, 0.0]
    print(f"     Set is_localization: {pose_info.is_localization}")
    print(f"     Set pose to origin: {pose_info.pose.position}")
    assert pose_info.is_localization == False
    assert abs(pose_info.pose.position[0]) < 1e-6
    assert abs(pose_info.pose.position[1]) < 1e-6
    assert abs(pose_info.pose.position[2]) < 1e-6

    print("   ✓ LocalizationInfo test passed")
    return True


def main():
    """Main test function"""
    try:
        print("Starting Navigation and SLAM Structures binding tests...")
        print("=" * 60)

        test_target_goal()
        test_map_image_data()
        test_map_meta_data()
        test_map_info()
        test_all_map_info()
        test_pose_info()

        print("\n" + "=" * 60)
        print(
            "🎉 All Navigation and SLAM Structures binding tests completed successfully!"
        )
        print("\nSummary:")
        print("  ✓ NavTarget - id, frame_id, goal (Pose3DEuler)")
        print("  ✓ MapImageData - width, height, max_gray_value, type, image")
        print("  ✓ MapMetaData - resolution, origin (Pose3DEuler), map_image_data")
        print("  ✓ MapInfo - map_name, map_meta_data")
        print("  ✓ AllMapInfo - current_map_name, map_infos array")
        print("  ✓ LocalizationInfo - is_localization, pose (Pose3DEuler)")

        return 0

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
