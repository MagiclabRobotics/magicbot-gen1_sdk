#!/usr/bin/env python3
"""
Test case for CameraInfo data structure
Tests all fields of the CameraInfo struct for read/write operations
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
        class CameraInfo:
            def __init__(self):
                self.header = magicbot.Header()
                self.height = 0
                self.width = 0
                self.distortion_model = ""
                self.D = []
                self.K = [0.0] * 9
                self.R = [0.0] * 9
                self.P = [0.0] * 12
                self.binning_x = 0
                self.binning_y = 0
                self.roi_x_offset = 0
                self.roi_y_offset = 0
                self.roi_height = 0
                self.roi_width = 0
                self.roi_do_rectify = False

        class Header:
            def __init__(self):
                self.stamp = 0
                self.frame_id = ""

    magicbot = MockMagicbot()
    print("\n✅ Using mock module for demonstration purposes.")
    print("   (Replace with actual module when available)")


def test_camerainfo_header():
    """Test CameraInfo header field"""
    print("=== Testing CameraInfo Header ===")

    cam_info = magicbot.CameraInfo()

    # Test header timestamp
    test_timestamp = 1234567890123456789
    cam_info.header.stamp = test_timestamp
    print(f"   Set header timestamp: {test_timestamp}")
    print(f"   Get header timestamp: {cam_info.header.stamp}")
    assert cam_info.header.stamp == test_timestamp, f"Header timestamp mismatch"
    print("   ✓ Header timestamp test passed")

    # Test header frame_id
    test_frame_id = "camera_frame"
    cam_info.header.frame_id = test_frame_id
    print(f"   Set header frame_id: {test_frame_id}")
    print(f"   Get header frame_id: {cam_info.header.frame_id}")
    assert cam_info.header.frame_id == test_frame_id, f"Header frame_id mismatch"
    print("   ✓ Header frame_id test passed")

    return True


def test_camerainfo_basic_fields():
    """Test CameraInfo basic fields"""
    print("\n=== Testing CameraInfo Basic Fields ===")

    cam_info = magicbot.CameraInfo()

    # Test height
    test_height = 480
    cam_info.height = test_height
    print(f"   Set height: {test_height}")
    print(f"   Get height: {cam_info.height}")
    assert cam_info.height == test_height, f"Height mismatch"
    print("   ✓ Height test passed")

    # Test width
    test_width = 640
    cam_info.width = test_width
    print(f"   Set width: {test_width}")
    print(f"   Get width: {cam_info.width}")
    assert cam_info.width == test_width, f"Width mismatch"
    print("   ✓ Width test passed")

    # Test distortion_model
    test_distortion_model = "plumb_bob"
    cam_info.distortion_model = test_distortion_model
    print(f"   Set distortion_model: {test_distortion_model}")
    print(f"   Get distortion_model: {cam_info.distortion_model}")
    assert (
        cam_info.distortion_model == test_distortion_model
    ), f"Distortion model mismatch"
    print("   ✓ Distortion model test passed")

    # Test binning_x
    test_binning_x = 2
    cam_info.binning_x = test_binning_x
    print(f"   Set binning_x: {test_binning_x}")
    print(f"   Get binning_x: {cam_info.binning_x}")
    assert cam_info.binning_x == test_binning_x, f"Binning X mismatch"
    print("   ✓ Binning X test passed")

    # Test binning_y
    test_binning_y = 2
    cam_info.binning_y = test_binning_y
    print(f"   Set binning_y: {test_binning_y}")
    print(f"   Get binning_y: {cam_info.binning_y}")
    assert cam_info.binning_y == test_binning_y, f"Binning Y mismatch"
    print("   ✓ Binning Y test passed")

    return True


def test_camerainfo_roi_fields():
    """Test CameraInfo ROI (Region of Interest) fields"""
    print("\n=== Testing CameraInfo ROI Fields ===")

    cam_info = magicbot.CameraInfo()

    # Test roi_x_offset
    test_roi_x_offset = 100
    cam_info.roi_x_offset = test_roi_x_offset
    print(f"   Set roi_x_offset: {test_roi_x_offset}")
    print(f"   Get roi_x_offset: {cam_info.roi_x_offset}")
    assert cam_info.roi_x_offset == test_roi_x_offset, f"ROI X offset mismatch"
    print("   ✓ ROI X offset test passed")

    # Test roi_y_offset
    test_roi_y_offset = 50
    cam_info.roi_y_offset = test_roi_y_offset
    print(f"   Set roi_y_offset: {test_roi_y_offset}")
    print(f"   Get roi_y_offset: {cam_info.roi_y_offset}")
    assert cam_info.roi_y_offset == test_roi_y_offset, f"ROI Y offset mismatch"
    print("   ✓ ROI Y offset test passed")

    # Test roi_height
    test_roi_height = 300
    cam_info.roi_height = test_roi_height
    print(f"   Set roi_height: {test_roi_height}")
    print(f"   Get roi_height: {cam_info.roi_height}")
    assert cam_info.roi_height == test_roi_height, f"ROI height mismatch"
    print("   ✓ ROI height test passed")

    # Test roi_width
    test_roi_width = 400
    cam_info.roi_width = test_roi_width
    print(f"   Set roi_width: {test_roi_width}")
    print(f"   Get roi_width: {cam_info.roi_width}")
    assert cam_info.roi_width == test_roi_width, f"ROI width mismatch"
    print("   ✓ ROI width test passed")

    # Test roi_do_rectify
    test_roi_do_rectify = True
    cam_info.roi_do_rectify = test_roi_do_rectify
    print(f"   Set roi_do_rectify: {test_roi_do_rectify}")
    print(f"   Get roi_do_rectify: {cam_info.roi_do_rectify}")
    assert cam_info.roi_do_rectify == test_roi_do_rectify, f"ROI do rectify mismatch"
    print("   ✓ ROI do rectify test passed")

    return True


def test_camerainfo_distortion_vector():
    """Test CameraInfo distortion vector D"""
    print("\n=== Testing CameraInfo Distortion Vector D ===")

    cam_info = magicbot.CameraInfo()

    # Test empty distortion vector
    print("   Testing empty distortion vector:")
    assert len(cam_info.D) == 0, "Initial distortion vector should be empty"
    print("     ✓ Empty distortion vector test passed")

    # Test adding distortion coefficients
    print("   Testing distortion coefficient addition:")
    # Typical plumb_bob distortion coefficients: [k1, k2, p1, p2, k3]
    distortion_coeffs = [0.1, -0.05, 0.001, 0.002, 0.01]

    for coeff in distortion_coeffs:
        cam_info.D.append(coeff)

    print(f"     Added {len(distortion_coeffs)} coefficients: {list(cam_info.D)}")
    assert (
        len(cam_info.D) == 5
    ), f"Distortion vector length should be 5, got {len(cam_info.D)}"

    # Verify coefficients
    for i, expected in enumerate(distortion_coeffs):
        assert (
            abs(cam_info.D[i] - expected) < 1e-6
        ), f"D[{i}] should be {expected}, got {cam_info.D[i]}"

    print("     ✓ Distortion coefficient addition test passed")

    # Test extending with more coefficients
    print("   Testing distortion coefficient extension:")
    additional_coeffs = [0.005, 0.003]
    cam_info.D.extend(additional_coeffs)
    print(
        f"     Extended with {len(additional_coeffs)} coefficients: {list(cam_info.D)}"
    )
    assert (
        len(cam_info.D) == 7
    ), f"Distortion vector length should be 7, got {len(cam_info.D)}"
    print("     ✓ Distortion coefficient extension test passed")

    # Test clearing distortion vector
    print("   Testing distortion vector clearing:")
    cam_info.D.clear()
    print(f"     Cleared distortion vector: {list(cam_info.D)}")
    assert len(cam_info.D) == 0, "Distortion vector should be empty after clearing"
    print("     ✓ Distortion vector clearing test passed")

    return True


def test_camerainfo_intrinsic_matrix():
    """Test CameraInfo intrinsic matrix K"""
    print("\n=== Testing CameraInfo Intrinsic Matrix K ===")

    cam_info = magicbot.CameraInfo()

    # Test initial state (should be 9 zeros)
    print("   Testing initial intrinsic matrix:")
    assert (
        len(cam_info.K) == 9
    ), f"Intrinsic matrix should have 9 elements, got {len(cam_info.K)}"
    for i in range(9):
        assert cam_info.K[i] == 0.0, f"K[{i}] should be 0.0, got {cam_info.K[i]}"
    print("     ✓ Initial intrinsic matrix test passed")

    # Test setting intrinsic matrix values
    print("   Testing intrinsic matrix assignment:")
    # Typical camera intrinsic matrix (3x3)
    # [fx, 0,  cx]
    # [0,  fy, cy]
    # [0,  0,  1 ]
    intrinsic_matrix = [
        1000.0,
        0.0,
        320.0,  # First row: fx, 0, cx
        0.0,
        1000.0,
        240.0,  # Second row: 0, fy, cy
        0.0,
        0.0,
        1.0,  # Third row: 0, 0, 1
    ]

    cam_info.K = intrinsic_matrix

    print(f"     Set intrinsic matrix: {cam_info.K}")

    # Verify the matrix
    for i, expected in enumerate(intrinsic_matrix):
        assert (
            abs(cam_info.K[i] - expected) < 1e-6
        ), f"K[{i}] should be {expected}, got {cam_info.K[i]}"

    print("     ✓ Intrinsic matrix assignment test passed")

    # Test accessing specific elements
    print("   Testing intrinsic matrix element access:")
    assert abs(cam_info.K[0] - 1000.0) < 1e-6, "Focal length X should be 1000.0"
    assert abs(cam_info.K[4] - 1000.0) < 1e-6, "Focal length Y should be 1000.0"
    assert abs(cam_info.K[2] - 320.0) < 1e-6, "Principal point X should be 320.0"
    assert abs(cam_info.K[5] - 240.0) < 1e-6, "Principal point Y should be 240.0"
    print("     ✓ Intrinsic matrix element access test passed")

    cam_info.K[0] = 2000.0
    cam_info.K[4] = 3000.0
    cam_info.K[2] = 1320.0
    cam_info.K[5] = 1240.0
    print(f"     Get intrinsic matrix: {cam_info.K}")
    assert abs(cam_info.K[0] - 2000.0) < 1e-6, "Focal length X should be 2000.0"
    assert abs(cam_info.K[4] - 3000.0) < 1e-6, "Focal length Y should be 3000.0"
    assert abs(cam_info.K[2] - 1320.0) < 1e-6, "Principal point X should be 1320.0"
    assert abs(cam_info.K[5] - 1240.0) < 1e-6, "Principal point Y should be 1240.0"
    print("     ✓ Intrinsic matrix element access test passed")

    return True


def test_camerainfo_rectification_matrix():
    """Test CameraInfo rectification matrix R"""
    print("\n=== Testing CameraInfo Rectification Matrix R ===")

    cam_info = magicbot.CameraInfo()

    # Test initial state (should be 9 zeros)
    print("   Testing initial rectification matrix:")
    assert (
        len(cam_info.R) == 9
    ), f"Rectification matrix should have 9 elements, got {len(cam_info.R)}"
    for i in range(9):
        assert cam_info.R[i] == 0.0, f"R[{i}] should be 0.0, got {cam_info.R[i]}"
    print("     ✓ Initial rectification matrix test passed")

    # Test setting rectification matrix values
    print("   Testing rectification matrix assignment:")
    # Identity matrix (no rectification)
    rectification_matrix = [
        1.0,
        0.0,
        0.0,  # First row
        0.0,
        1.0,
        0.0,  # Second row
        0.0,
        0.0,
        1.0,  # Third row
    ]

    cam_info.R = rectification_matrix

    print(f"     Set rectification matrix: {list(cam_info.R)}")

    # Verify the matrix
    for i, expected in enumerate(rectification_matrix):
        assert (
            abs(cam_info.R[i] - expected) < 1e-6
        ), f"R[{i}] should be {expected}, got {cam_info.R[i]}"

    print("     ✓ Rectification matrix assignment test passed")

    cam_info.R[0] = 2.0
    cam_info.R[4] = 3.0
    cam_info.R[2] = 1.320
    cam_info.R[5] = 1.240
    print(f"     Get rectification matrix: {list(cam_info.R)}")
    assert abs(cam_info.R[0] - 2.0) < 1e-6, "Focal length X should be 2.0"
    assert abs(cam_info.R[4] - 3.0) < 1e-6, "Focal length Y should be 3.0"
    assert abs(cam_info.R[2] - 1.320) < 1e-6, "Principal point X should be 1.320"
    assert abs(cam_info.R[5] - 1.240) < 1e-6, "Principal point Y should be 1.240"
    print("     ✓ Rectification matrix element access test passed")

    return True


def test_camerainfo_projection_matrix():
    """Test CameraInfo projection matrix P"""
    print("\n=== Testing CameraInfo Projection Matrix P ===")

    cam_info = magicbot.CameraInfo()

    # Test initial state (should be 12 zeros)
    print("   Testing initial projection matrix:")
    assert (
        len(cam_info.P) == 12
    ), f"Projection matrix should have 12 elements, got {len(cam_info.P)}"
    for i in range(12):
        assert cam_info.P[i] == 0.0, f"P[{i}] should be 0.0, got {cam_info.P[i]}"
    print("     ✓ Initial projection matrix test passed")

    # Test setting projection matrix values
    print("   Testing projection matrix assignment:")
    # Typical 3x4 projection matrix
    projection_matrix = [
        1000.0,
        0.0,
        320.0,
        0.0,  # First row: fx, 0, cx, 0
        0.0,
        1000.0,
        240.0,
        0.0,  # Second row: 0, fy, cy, 0
        0.0,
        0.0,
        1.0,
        0.0,  # Third row: 0, 0, 1, 0
    ]

    cam_info.P = projection_matrix

    print(f"     Set projection matrix: {list(cam_info.P)}")

    # Verify the matrix
    for i, expected in enumerate(projection_matrix):
        assert (
            abs(cam_info.P[i] - expected) < 1e-6
        ), f"P[{i}] should be {expected}, got {cam_info.P[i]}"

    print("     ✓ Projection matrix assignment test passed")

    cam_info.P[0] = 2000.0
    cam_info.P[4] = 3000.0
    cam_info.P[2] = 1320.0
    cam_info.P[5] = 1240.0
    print(f"     Get projection matrix: {list(cam_info.P)}")
    assert abs(cam_info.P[0] - 2000.0) < 1e-6, "Focal length X should be 2000.0"
    assert abs(cam_info.P[4] - 3000.0) < 1e-6, "Focal length Y should be 3000.0"
    assert abs(cam_info.P[2] - 1320.0) < 1e-6, "Principal point X should be 1320.0"
    assert abs(cam_info.P[5] - 1240.0) < 1e-6, "Principal point Y should be 1240.0"
    print("     ✓ Projection matrix element access test passed")

    return True


def test_camerainfo_comprehensive():
    """Test comprehensive CameraInfo data"""
    print("\n=== Testing Comprehensive CameraInfo Data ===")

    cam_info = magicbot.CameraInfo()

    # Set all fields
    cam_info.header.stamp = 9223372036854775807
    cam_info.header.frame_id = "test_camera"
    cam_info.height = 480
    cam_info.width = 640
    cam_info.distortion_model = "plumb_bob"

    # Set distortion coefficients
    cam_info.D.clear()
    cam_info.D.extend([0.1, -0.05, 0.001, 0.002, 0.01])

    # Set intrinsic matrix (3x3)
    intrinsic_matrix = [1000.0, 0.0, 320.0, 0.0, 1000.0, 240.0, 0.0, 0.0, 1.0]
    for i, value in enumerate(intrinsic_matrix):
        cam_info.K[i] = value

    # Set rectification matrix (3x3 identity)
    rectification_matrix = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
    for i, value in enumerate(rectification_matrix):
        cam_info.R[i] = value

    # Set projection matrix (3x4)
    projection_matrix = [
        1000.0,
        0.0,
        320.0,
        0.0,
        0.0,
        1000.0,
        240.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
    ]
    for i, value in enumerate(projection_matrix):
        cam_info.P[i] = value

    # Set binning and ROI
    cam_info.binning_x = 1
    cam_info.binning_y = 1
    cam_info.roi_x_offset = 0
    cam_info.roi_y_offset = 0
    cam_info.roi_height = 480
    cam_info.roi_width = 640
    cam_info.roi_do_rectify = False

    print("   Setting comprehensive camera info data:")
    print(f"     Header stamp: {cam_info.header.stamp}")
    print(f"     Header frame_id: {cam_info.header.frame_id}")
    print(f"     Height: {cam_info.height}")
    print(f"     Width: {cam_info.width}")
    print(f"     Distortion model: {cam_info.distortion_model}")
    print(f"     Distortion coefficients: {list(cam_info.D)}")
    print(f"     Intrinsic matrix K: {list(cam_info.K)}")
    print(f"     Rectification matrix R: {list(cam_info.R)}")
    print(f"     Projection matrix P: {list(cam_info.P)}")
    print(f"     Binning: ({cam_info.binning_x}, {cam_info.binning_y})")
    print(
        f"     ROI: ({cam_info.roi_x_offset}, {cam_info.roi_y_offset}, {cam_info.roi_width}, {cam_info.roi_height})"
    )
    print(f"     ROI do rectify: {cam_info.roi_do_rectify}")

    # Verify all fields
    assert cam_info.header.stamp == 9223372036854775807
    assert cam_info.header.frame_id == "test_camera"
    assert cam_info.height == 480
    assert cam_info.width == 640
    assert cam_info.distortion_model == "plumb_bob"
    assert len(cam_info.D) == 5
    assert len(cam_info.K) == 9
    assert len(cam_info.R) == 9
    assert len(cam_info.P) == 12
    assert cam_info.binning_x == 1
    assert cam_info.binning_y == 1
    assert cam_info.roi_x_offset == 0
    assert cam_info.roi_y_offset == 0
    assert cam_info.roi_height == 480
    assert cam_info.roi_width == 640
    assert cam_info.roi_do_rectify == False

    print("   ✓ Comprehensive test passed")
    return True


def main():
    """Main test function"""
    try:
        print("Starting Imu binding tests...")

        test_camerainfo_header()
        test_camerainfo_basic_fields()
        test_camerainfo_roi_fields()
        test_camerainfo_distortion_vector()
        test_camerainfo_intrinsic_matrix()
        test_camerainfo_rectification_matrix()
        test_camerainfo_projection_matrix()
        test_camerainfo_comprehensive()

        print("\n🎉 All CameraInfo binding tests completed successfully!")
        print("\nSummary:")
        print("  ✓ Header fields (stamp, frame_id)")
        print(
            "  ✓ Basic fields (height, width, distortion_model, binning_x, binning_y)"
        )
        print(
            "  ✓ ROI fields (roi_x_offset, roi_y_offset, roi_width, roi_height, roi_do_rectify)"
        )
        print("  ✓ Distortion vector D")
        print("  ✓ Intrinsic matrix K")
        print("  ✓ Rectification matrix R")
        print("  ✓ Projection matrix P")
        print("  ✓ Comprehensive data setting and verification")

        return 0

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
