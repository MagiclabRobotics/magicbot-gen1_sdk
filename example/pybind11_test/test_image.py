#!/usr/bin/env python3
"""
Test case for Image data structure
Tests all fields of the Image struct for read/write operations
"""

import sys
import os

# Add the parent directory to the path to import magicbot_gen1_python
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    import magicbot_gen1_python as magicbot
except ImportError as e:
    print(f"Error importing magicbot_gen1_python: {e}")
    print("Please make sure the module is built and installed correctly.")
    sys.exit(1)

def test_image_header():
    """Test Image header field"""
    print("=== Testing Image Header ===")
    
    image = magicbot.Image()
    
    # Test header timestamp
    test_timestamp = 1234567890123456789
    image.header.stamp = test_timestamp
    print(f"   Set header timestamp: {test_timestamp}")
    print(f"   Get header timestamp: {image.header.stamp}")
    assert image.header.stamp == test_timestamp, f"Header timestamp mismatch"
    print("   ✓ Header timestamp test passed")
    
    # Test header frame_id
    test_frame_id = "camera_frame"
    image.header.frame_id = test_frame_id
    print(f"   Set header frame_id: {test_frame_id}")
    print(f"   Get header frame_id: {image.header.frame_id}")
    assert image.header.frame_id == test_frame_id, f"Header frame_id mismatch"
    print("   ✓ Header frame_id test passed")
    
    return True

def test_image_basic_fields():
    """Test Image basic fields"""
    print("\n=== Testing Image Basic Fields ===")
    
    image = magicbot.Image()
    
    # Test height
    test_height = 480
    image.height = test_height
    print(f"   Set height: {test_height}")
    print(f"   Get height: {image.height}")
    assert image.height == test_height, f"Height mismatch"
    print("   ✓ Height test passed")
    
    # Test width
    test_width = 640
    image.width = test_width
    print(f"   Set width: {test_width}")
    print(f"   Get width: {image.width}")
    assert image.width == test_width, f"Width mismatch"
    print("   ✓ Width test passed")
    
    # Test encoding
    test_encoding = "rgb8"
    image.encoding = test_encoding
    print(f"   Set encoding: {test_encoding}")
    print(f"   Get encoding: {image.encoding}")
    assert image.encoding == test_encoding, f"Encoding mismatch"
    print("   ✓ Encoding test passed")
    
    # Test is_bigendian
    test_is_bigendian = True
    image.is_bigendian = test_is_bigendian
    print(f"   Set is_bigendian: {test_is_bigendian}")
    print(f"   Get is_bigendian: {image.is_bigendian}")
    assert image.is_bigendian == test_is_bigendian, f"is_bigendian mismatch"
    print("   ✓ is_bigendian test passed")
    
    # Test step
    test_step = 1920  # 640 * 3 bytes per pixel for RGB
    image.step = test_step
    print(f"   Set step: {test_step}")
    print(f"   Get step: {image.step}")
    assert image.step == test_step, f"Step mismatch"
    print("   ✓ Step test passed")
    
    return True

def test_image_data():
    """Test Image data field"""
    print("\n=== Testing Image Data ===")
    
    image = magicbot.Image()
    
    # Test empty data
    print("   Testing empty data:")
    assert len(image.data) == 0, "Initial data should be empty"
    print("     ✓ Empty data test passed")
    
    # Test adding single bytes
    print("   Testing single byte addition:")
    image.data.append(255)  # White pixel component
    image.data.append(128)  # Gray pixel component
    image.data.append(0)    # Black pixel component
    print(f"     Added 3 bytes: {list(image.data)}")  # Convert to list for safe printing
    assert len(image.data) == 3, f"Data length should be 3, got {len(image.data)}"
    assert image.data[0] == 255, f"First byte should be 255, got {image.data[0]}"
    assert image.data[1] == 128, f"Second byte should be 128, got {image.data[1]}"
    assert image.data[2] == 0, f"Third byte should be 0, got {image.data[2]}"
    print("     ✓ Single byte addition test passed")
    
    # Test extending with multiple bytes
    print("   Testing multiple byte extension:")
    additional_bytes = [100, 150, 200, 50, 75, 125]
    image.data.extend(additional_bytes)
    print(f"     Extended with {len(additional_bytes)} bytes: {list(image.data)}")  # Convert to list for safe printing
    assert len(image.data) == 9, f"Data length should be 9, got {len(image.data)}"
    print("     ✓ Multiple byte extension test passed")
    
    # Test direct assignment
    print("   Testing direct data assignment:")
    new_data = [1, 2, 3, 4, 5]
    image.data.clear()
    image.data.extend(new_data)
    print(f"     Assigned new data: {list(image.data)}")  # Convert to list for safe printing
    assert len(image.data) == 5, f"Data length should be 5, got {len(image.data)}"
    for i, expected in enumerate(new_data):
        assert image.data[i] == expected, f"Data[{i}] should be {expected}, got {image.data[i]}"
    print("     ✓ Direct data assignment test passed")
    
    # Test clearing data
    print("   Testing data clearing:")
    image.data.clear()
    print(f"     Cleared data: {list(image.data)}")  # Convert to list for safe printing
    assert len(image.data) == 0, "Data should be empty after clearing"
    print("     ✓ Data clearing test passed")
    
    return True

def test_image_simulated_rgb():
    """Test Image with simulated RGB data"""
    print("\n=== Testing Image with Simulated RGB Data ===")
    
    image = magicbot.Image()
    
    # Set up a small RGB image (2x2 pixels)
    image.height = 2
    image.width = 2
    image.encoding = "rgb8"
    image.is_bigendian = False
    image.step = 6  # 2 pixels * 3 bytes per pixel
    
    # Create RGB data for 2x2 image (4 pixels, 12 bytes total)
    # Pixel 1: Red (255, 0, 0)
    # Pixel 2: Green (0, 255, 0)
    # Pixel 3: Blue (0, 0, 255)
    # Pixel 4: White (255, 255, 255)
    rgb_data = [
        255, 0, 0,    # Pixel 1: Red
        0, 255, 0,    # Pixel 2: Green
        0, 0, 255,    # Pixel 3: Blue
        255, 255, 255 # Pixel 4: White
    ]
    
    image.data.clear()
    image.data.extend(rgb_data)
    print(f"   Created 2x2 RGB image:")
    print(f"     Height: {image.height}")
    print(f"     Width: {image.width}")
    print(f"     Encoding: {image.encoding}")
    print(f"     Step: {image.step}")
    print(f"     Data length: {len(image.data)} bytes")
    print(f"     Data: {list(image.data)}")
    
    # Verify the data
    assert image.height == 2, f"Height should be 2, got {image.height}"
    assert image.width == 2, f"Width should be 2, got {image.width}"
    assert image.encoding == "rgb8", f"Encoding should be 'rgb8', got {image.encoding}"
    assert image.step == 6, f"Step should be 6, got {image.step}"
    assert len(image.data) == 12, f"Data length should be 12, got {len(image.data)}"
    
    # Verify pixel values
    assert list(image.data[0:3]) == [255, 0, 0], f"Pixel 1 should be red, got {list(image.data[0:3])}"
    assert list(image.data[3:6]) == [0, 255, 0], f"Pixel 2 should be green, got {list(image.data[3:6])}"
    assert list(image.data[6:9]) == [0, 0, 255], f"Pixel 3 should be blue, got {list(image.data[6:9])}"
    assert list(image.data[9:12]) == [255, 255, 255], f"Pixel 4 should be white, got {list(image.data[9:12])}"
    
    print("   ✓ Simulated RGB image test passed")
    return True

def test_image_edge_cases():
    """Test Image edge cases"""
    print("\n=== Testing Image Edge Cases ===")
    
    image = magicbot.Image()
    
    # Test zero dimensions
    print("   Testing zero dimensions:")
    image.height = 0
    image.width = 0
    image.step = 0
    print(f"     Set zero dimensions: height={image.height}, width={image.width}, step={image.step}")
    assert image.height == 0, f"Height should be 0, got {image.height}"
    assert image.width == 0, f"Width should be 0, got {image.width}"
    assert image.step == 0, f"Step should be 0, got {image.step}"
    print("     ✓ Zero dimensions test passed")
    
    # Test large dimensions
    print("   Testing large dimensions:")
    image.height = 1920
    image.width = 1080
    image.step = 3240  # 1080 * 3 bytes per pixel
    print(f"     Set large dimensions: height={image.height}, width={image.width}, step={image.step}")
    assert image.height == 1920, f"Height should be 1920, got {image.height}"
    assert image.width == 1080, f"Width should be 1080, got {image.width}"
    assert image.step == 3240, f"Step should be 3240, got {image.step}"
    print("     ✓ Large dimensions test passed")
    
    # Test different encodings
    print("   Testing different encodings:")
    encodings = ["mono8", "bgr8", "bgra8", "rgba8", "yuv422"]
    for encoding in encodings:
        image.encoding = encoding
        print(f"     Set encoding: {image.encoding}")
        assert image.encoding == encoding, f"Encoding should be '{encoding}', got '{image.encoding}'"
    print("     ✓ Different encodings test passed")
    
    # Test empty string encoding
    print("   Testing empty string encoding:")
    image.encoding = ""
    print(f"     Set empty encoding: '{image.encoding}'")
    assert image.encoding == "", f"Encoding should be empty string, got '{image.encoding}'"
    print("     ✓ Empty string encoding test passed")
    
    print("   ✓ Edge cases test passed")
    return True

def test_image_comprehensive():
    """Test comprehensive Image data"""
    print("\n=== Testing Comprehensive Image Data ===")
    
    image = magicbot.Image()
    
    # Set all fields
    image.header.stamp = 11111111111
    image.header.frame_id = "test_camera"
    image.height = 480
    image.width = 640
    image.encoding = "rgb8"
    image.is_bigendian = False
    image.step = 1920
    
    # Create some test image data
    test_data = [i % 256 for i in range(100)]  # 100 bytes of test data
    image.data.clear()
    image.data.extend(test_data)

    
    print("   Setting comprehensive image data:")
    print(f"     Header stamp: {image.header.stamp}")
    print(f"     Header frame_id: {image.header.frame_id}")
    print(f"     Height: {image.height}")
    print(f"     Width: {image.width}")
    print(f"     Encoding: {image.encoding}")
    print(f"     is_bigendian: {image.is_bigendian}")
    print(f"     Step: {image.step}")
    print(f"     Data length: {len(image.data)}")
    print(f"     First 10 data bytes: {image.data[:10]}")
    
    # Verify all fields
    assert image.header.stamp == 11111111111
    assert image.header.frame_id == "test_camera"
    assert image.height == 480
    assert image.width == 640
    assert image.encoding == "rgb8"
    assert image.is_bigendian == False
    assert image.step == 1920
    assert len(image.data) == 100
    
    # Verify data pattern
    for i in range(100):
        assert image.data[i] == i % 256, f"Data[{i}] should be {i % 256}, got {image.data[i]}"
    
    print("   ✓ Comprehensive test passed")
    return True

def main():
    """Main test function"""
    try:
        print("Starting Image binding tests...")
        print("=" * 50)
        
        test_image_header()
        test_image_basic_fields()
        test_image_data()
        test_image_simulated_rgb()
        test_image_edge_cases()
        test_image_comprehensive()
        
        print("\n" + "=" * 50)
        print("🎉 All Image binding tests completed successfully!")
        print("\nSummary:")
        print("  ✓ Header fields (stamp, frame_id)")
        print("  ✓ Basic fields (height, width, encoding, is_bigendian, step)")
        print("  ✓ Data field (append, extend, clear, assignment)")
        print("  ✓ Simulated RGB image data")
        print("  ✓ Edge cases (zero/large dimensions, different encodings)")
        print("  ✓ Comprehensive data setting and verification")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
