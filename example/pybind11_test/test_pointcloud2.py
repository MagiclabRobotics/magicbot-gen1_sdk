#!/usr/bin/env python3

import sys
import magicbot_gen1_python as magicbot

def test_pointcloud2_fields():
    """Test PointCloud2 field read/write operations"""
    print("Testing PointCloud2 field read/write operations...")
    
    # Create a PointCloud2 instance
    pointcloud = magicbot.PointCloud2()
    print(f"Created PointCloud2 instance: {pointcloud}")
    
    # Test 1: Header field
    print("\n=== Test 1: Header field ===")
    print(f"Initial header stamp: {pointcloud.header.stamp}")
    print(f"Initial header frame_id: {pointcloud.header.frame_id}")
    
    pointcloud.header.frame_id = "test_header"
    pointcloud.header.stamp = 1234567890
    print(f"After setting header - stamp: {pointcloud.header.stamp}")
    print(f"After setting header - frame_id: {pointcloud.header.frame_id}")
    
    assert pointcloud.header.frame_id == "test_header", "Header frame_id test failed"
    assert pointcloud.header.stamp == 1234567890, "Header stamp test failed"
    print("✓ Header field test passed")
    
    # Test 2: Height field
    print("\n=== Test 2: Height field ===")
    print(f"Initial height: {pointcloud.height}")
    pointcloud.height = 480
    print(f"After setting height: {pointcloud.height}")
    assert pointcloud.height == 480, "Height field test failed"
    print("✓ Height field test passed")
    
    # Test 3: Width field
    print("\n=== Test 3: Width field ===")
    print(f"Initial width: {pointcloud.width}")
    pointcloud.width = 640
    print(f"After setting width: {pointcloud.width}")
    assert pointcloud.width == 640, "Width field test failed"
    print("✓ Width field test passed")
    
    # Test 4: Fields array (PointField objects)
    print("\n=== Test 4: Fields array ===")
    print(f"Initial fields length: {len(pointcloud.fields)}")
    
    # Create and add PointField objects
    field_names = ["x", "y", "z", "intensity"]
    field_offsets = [0, 4, 8, 12]  # 4 bytes per float
    field_datatypes = [7, 7, 7, 7]  # FLOAT32 = 7
    field_counts = [1, 1, 1, 1]
    
    for i, name in enumerate(field_names):
        field = magicbot.PointField()
        field.name = name
        field.offset = field_offsets[i]
        field.datatype = field_datatypes[i]
        field.count = field_counts[i]
        pointcloud.fields.append(field)
        # pointcloud.add_field(field)

        print(f"Added field '{name}' at offset {field.offset}, current length: {len(pointcloud.fields)}")
    
    print(f"Final fields count: {len(pointcloud.fields)}")
    assert len(pointcloud.fields) == 4, "Fields array test failed"
    
    # Verify field contents
    for i, field in enumerate(pointcloud.fields):
        assert field.name == field_names[i], f"Field {i} name test failed"
        assert field.offset == field_offsets[i], f"Field {i} offset test failed"
        assert field.datatype == field_datatypes[i], f"Field {i} datatype test failed"
        assert field.count == field_counts[i], f"Field {i} count test failed"
    
    print("✓ Fields array test passed")
    
    # Test 5: is_bigendian field
    print("\n=== Test 5: is_bigendian field ===")
    print(f"Initial is_bigendian: {pointcloud.is_bigendian}")
    pointcloud.is_bigendian = True
    print(f"After setting is_bigendian: {pointcloud.is_bigendian}")
    assert pointcloud.is_bigendian == True, "is_bigendian field test failed"
    
    pointcloud.is_bigendian = False
    print(f"After setting is_bigendian to False: {pointcloud.is_bigendian}")
    assert pointcloud.is_bigendian == False, "is_bigendian field test failed"
    print("✓ is_bigendian field test passed")
    
    # Test 6: point_step field
    print("\n=== Test 6: point_step field ===")
    print(f"Initial point_step: {pointcloud.point_step}")
    pointcloud.point_step = 16
    print(f"After setting point_step: {pointcloud.point_step}")
    assert pointcloud.point_step == 16, "point_step field test failed"
    print("✓ point_step field test passed")
    
    # Test 7: row_step field
    print("\n=== Test 7: row_step field ===")
    print(f"Initial row_step: {pointcloud.row_step}")
    pointcloud.row_step = 10240  # 640 * 16
    print(f"After setting row_step: {pointcloud.row_step}")
    assert pointcloud.row_step == 10240, "row_step field test failed"
    print("✓ row_step field test passed")
    
    # Test 8: Data array (uint8_t bytes)
    print("\n=== Test 8: Data array ===")
    print(f"Initial data length: {len(pointcloud.data)}")
    
    # Add some test byte data (simulating point cloud data)
    # Create 4 points with x,y,z,intensity (4 floats * 4 bytes = 16 bytes per point)
    import struct
    
    test_points = [
        (1.0, 2.0, 3.0, 255.0),  # Point 1
        (4.0, 5.0, 6.0, 128.0),  # Point 2
        (7.0, 8.0, 9.0, 64.0),   # Point 3
        (10.0, 11.0, 12.0, 32.0) # Point 4
    ]
    
    for point in test_points:
        # Pack each point as 4 floats (16 bytes)
        point_bytes = struct.pack('ffff', *point)
        # pointcloud.add_data_bytes(point_bytes)
        for i in range(16):
            pointcloud.data.append(point_bytes[i])
        print(f"Added point {point}, current data length: {len(pointcloud.data)} bytes")
    
    print(f"Final data length: {len(pointcloud.data)} bytes")
    assert len(pointcloud.data) == 64, "Data array test failed"  # 4 points * 16 bytes
    
    # Verify first point data
    first_point_bytes = pointcloud.data[0:16]
    first_point = struct.unpack('ffff', bytes(first_point_bytes))
    assert first_point == (1.0, 2.0, 3.0, 255.0), "Data content test failed"
    print(f"First point unpacked: {first_point}")
    print("✓ Data array test passed")
    
    # Test 9: is_dense field
    print("\n=== Test 9: is_dense field ===")
    print(f"Initial is_dense: {pointcloud.is_dense}")
    pointcloud.is_dense = True
    print(f"After setting is_dense: {pointcloud.is_dense}")
    assert pointcloud.is_dense == True, "is_dense field test failed"
    
    pointcloud.is_dense = False
    print(f"After setting is_dense to False: {pointcloud.is_dense}")
    assert pointcloud.is_dense == False, "is_dense field test failed"
    print("✓ is_dense field test passed")
    
    return True

def main():
    """Main test function"""
    try:
        print("Starting PointCloud2 field read/write tests...")
        
        # Run basic field tests
        test_pointcloud2_fields()
    
        
        print("\n🎉 All PointCloud2 tests completed successfully!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
