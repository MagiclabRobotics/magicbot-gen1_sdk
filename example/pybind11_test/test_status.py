#!/usr/bin/env python3
"""
Simple test case for Status data structure
Tests basic read/write operations for all fields
"""

import sys
import os

# Add the parent directory to the path to import magicbot_gen1_python
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

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
    print("\n📝 For now, this test will show the expected structure without running actual tests.")
    
    # Create a mock module for demonstration
    class MockMagicbot:
        class Status:
            def __init__(self):
                self.code = 0
                self.message = ""
    
    magicbot = MockMagicbot()
    print("\n✅ Using mock module for demonstration purposes.")
    print("   (Replace with actual module when available)")

def test_status_initial_values():
    """Test Status initial values"""
    print("=== Testing Status Initial Values ===")
    
    status = magicbot.Status()
    
    # Test initial values
    print("   Testing initial values:")
    print(f"     code: {status.code}")
    print(f"     message: '{status.message}'")
    
    # Verify initial values
    assert status.code == 0
    assert status.message == ""
    
    print("   ✓ Initial values test passed")
    return True

def test_status_code():
    """Test Status code field"""
    print("\n=== Testing Status Code ===")
    
    status = magicbot.Status()
    
    # Test ErrorCode values
    print("   Testing ErrorCode values:")
    error_codes = {
        magicbot.ErrorCode.OK: "OK",
        magicbot.ErrorCode.SERVICE_NOT_READY: "SERVICE_NOT_READY", 
        magicbot.ErrorCode.TIMEOUT: "TIMEOUT",
        magicbot.ErrorCode.INTERNAL_ERROR: "INTERNAL_ERROR",
        magicbot.ErrorCode.SERVICE_ERROR: "SERVICE_ERROR"
    }
    
    for code, name in error_codes.items():
        status.code = code
        print(f"     Set code: {code} ({name})")
        print(f"     Get code: {status.code}")
        assert status.code == code, f"Code should be {code}, got {status.code}"
        print(f"     ✓ Code {code} ({name}) test passed")
    
    return True

def test_status_message():
    """Test Status message field"""
    print("\n=== Testing Status Message ===")
    
    status = magicbot.Status()
    
    # Test different message types
    print("   Testing different message types:")
    test_messages = [
        "",
        "Success",
        "Operation completed successfully",
        "Error occurred during processing",
        "Timeout: operation took too long",
        "Service is not ready",
        "Internal error in the system"
    ]
    
    for message in test_messages:
        status.message = message
        print(f"     Set message: '{message}'")
        print(f"     Get message: '{status.message}'")
        assert status.message == message, f"Message should be '{message}', got '{status.message}'"
        print(f"     ✓ Message '{message}' test passed")
    
    return True


def main():
    """Main test function"""
    try:
        print("Starting RobotState binding tests...")
        print("=" * 50)
        
        test_status_initial_values()
        test_status_code()
        test_status_message()
        
        print("\n" + "=" * 50)
        print("🎉 All RobotState binding tests completed successfully!")
        print("\nSummary:")
        print("  ✓ Status - code, message")
        print("  ✓ Status code - 0, 1, 2, 3, 4")
        print("  ✓ Status message - empty, Success, Operation completed successfully, Error occurred during processing, Timeout: operation took too long, Service is not ready, Internal error in the system")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
