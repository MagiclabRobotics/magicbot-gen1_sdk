# Example Description

This example demonstrates hybrid motion control functionality including gait control, joystick commands, upper body control, and hand control.

## Runtime Dependencies
export LD_LIBRARY_PATH=YOUR_PATH/magicbot_gen1_sdk/build:$LD_LIBRARY_PATH

## Example Execution

./hybrid_motion_example

After running the example, press keys to interact with the robot:

### Gait and Trick Functions:
- **0**: Get current gait mode
- **1**: Set recovery stand gait (GAIT_RECOVERY_STAND)
- **2**: Set hybrid gait (GAIT_HYBRID_SDK)

### Joystick Functions:
- **w/W**: Move forward
- **a/A**: Move left
- **s/S**: Move backward
- **d/D**: Move right
- **x/X**: Stop
- **t/T**: Turn left
- **g/G**: Turn right

### Upper Body Functions:
- **3**: Subscribe to upper body state
- **4**: Unsubscribe from upper body state
- **5**: Publish upper body command

### Hand Functions:
- **6**: Subscribe to all hand state
- **7**: Unsubscribe from all hand state
- **8**: Publish all hand command

### Other:
- **?**: Print help message
- **ESC**: Exit program

## Typical Usage Flow:

1. Switch from suspended state to recovery stand (press '1')
2. Switch from recovery stand state to hybrid gait (press '2')
3. Send joystick commands to control robot movement (press 'w', 'a', 's', 'd', 't', 'g', or 'x')
4. Control upper body joints (press '3' to subscribe, '5' to publish commands)
5. Control hands (press '6' to subscribe, '8' to publish commands)
