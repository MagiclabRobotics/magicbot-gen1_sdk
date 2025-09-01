#!/usr/bin/env python3
"""
Simple test case for TtsCommand data structure
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
        class TtsCommand:
            def __init__(self):
                self.id = ""
                self.content = ""
                self.priority = 0
                self.mode = 0
    
    magicbot = MockMagicbot()
    print("\n✅ Using mock module for demonstration purposes.")
    print("   (Replace with actual module when available)")

def test_tts_command_initial_values():
    """Test TtsCommand initial values"""
    print("=== Testing TtsCommand Initial Values ===")
    
    tts_cmd = magicbot.TtsCommand()
    
    # Test initial values
    print("   Testing initial values:")
    print(f"     id: '{tts_cmd.id}'")
    print(f"     content: '{tts_cmd.content}'")
    print(f"     priority: {tts_cmd.priority}")
    print(f"     mode: {tts_cmd.mode}")
    
    # Verify initial values
    assert tts_cmd.id == ""
    assert tts_cmd.content == ""
    assert tts_cmd.priority == magicbot.TtsPriority.HIGH
    assert tts_cmd.mode == magicbot.TtsMode.CLEARTOP
    
    print("   ✓ Initial values test passed")
    return True

def test_tts_command_id():
    """Test TtsCommand id field"""
    print("\n=== Testing TtsCommand ID ===")
    
    tts_cmd = magicbot.TtsCommand()
    
    # Test setting different IDs
    print("   Testing setting different IDs:")
    test_ids = ["id_01", "tts_task_001", "voice_alert_123", "welcome_message"]
    
    for test_id in test_ids:
        tts_cmd.id = test_id
        print(f"     Set id: '{tts_cmd.id}'")
        assert tts_cmd.id == test_id, f"ID should be '{test_id}', got '{tts_cmd.id}'"
        print(f"     ✓ ID '{test_id}' test passed")
    
    # Test empty ID
    tts_cmd.id = ""
    print(f"     Set empty id: '{tts_cmd.id}'")
    assert tts_cmd.id == ""
    print("     ✓ Empty ID test passed")
    
    return True

def test_tts_command_content():
    """Test TtsCommand content field"""
    print("\n=== Testing TtsCommand Content ===")
    
    tts_cmd = magicbot.TtsCommand()
    
    # Test setting different content
    print("   Testing setting different content:")
    test_contents = [
        "你好，欢迎使用智能语音系统。",
        "Hello, welcome to the intelligent voice system.",
        "Battery level is low, please charge soon.",
        "System is ready for operation.",
        "Warning: Obstacle detected ahead."
    ]
    
    for content in test_contents:
        tts_cmd.content = content
        print(f"     Set content: '{tts_cmd.content}'")
        assert tts_cmd.content == content, f"Content should be '{content}', got '{tts_cmd.content}'"
        print(f"     ✓ Content test passed")
    
    # Test empty content
    tts_cmd.content = ""
    print(f"     Set empty content: '{tts_cmd.content}'")
    assert tts_cmd.content == ""
    print("     ✓ Empty content test passed")
    
    return True

def test_tts_command_priority():
    """Test TtsCommand priority field"""
    print("\n=== Testing TtsCommand Priority ===")
    
    tts_cmd = magicbot.TtsCommand()
    
    # Test priority values (based on TtsPriority enum)
    print("   Testing priority values:")
    priorities = {
        magicbot.TtsPriority.HIGH: "HIGH",      # 最高优先级
        magicbot.TtsPriority.MIDDLE: "MIDDLE",    # 中优先级
        magicbot.TtsPriority.LOW: "LOW"        # 最低优先级
    }
    
    for priority_value, priority_name in priorities.items():
        tts_cmd.priority = priority_value
        print(f"     Set priority: {priority_value} ({priority_name})")
        print(f"     Get priority: {tts_cmd.priority}")
        assert tts_cmd.priority == priority_value, f"Priority should be {priority_value}, got {tts_cmd.priority}"
        print(f"     ✓ Priority {priority_value} ({priority_name}) test passed")
    
    return True

def test_tts_command_mode():
    """Test TtsCommand mode field"""
    print("\n=== Testing TtsCommand Mode ===")
    
    tts_cmd = magicbot.TtsCommand()
    
    # Test mode values (based on TtsMode enum)
    print("   Testing mode values:")
    modes = {
        magicbot.TtsMode.CLEARTOP: "CLEARTOP",     # 清空当前优先级所有任务
        magicbot.TtsMode.ADD: "ADD",          # 追加到队列尾部
        magicbot.TtsMode.CLEARBUFFER: "CLEARBUFFER"   # 清空队列中未播放的请求
    }
    
    for mode_value, mode_name in modes.items():
        tts_cmd.mode = mode_value
        print(f"     Set mode: {mode_value} ({mode_name})")
        print(f"     Get mode: {tts_cmd.mode}")
        assert tts_cmd.mode == mode_value, f"Mode should be {mode_value}, got {tts_cmd.mode}"
        print(f"     ✓ Mode {mode_value} ({mode_name}) test passed")
    
    return True


def main():
    """Main test function"""
    try:
        print("Starting RobotState binding tests...")
        print("=" * 50)
        
        test_tts_command_initial_values()
        test_tts_command_id()
        test_tts_command_content()
        test_tts_command_priority()
        test_tts_command_mode()
        
        print("\n" + "=" * 50)
        print("🎉 All RobotState binding tests completed successfully!")
        print("\nSummary:")
        print("  ✓ TtsCommand - id, content, priority, mode")
        print("  ✓ TtsCommand id - empty, id_01, tts_task_001, voice_alert_123, welcome_message")
        print("  ✓ TtsCommand content - empty, 你好，欢迎使用智能语音系统。, Hello, welcome to the intelligent voice system., Battery level is low, please charge soon., System is ready for operation., Warning: Obstacle detected ahead.")
        print("  ✓ TtsCommand priority - 0, 1, 2")
        print("  ✓ TtsCommand mode - 0, 1, 2")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
