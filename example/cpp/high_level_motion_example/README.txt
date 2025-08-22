# Example Description

## Runtime Dependencies
export LD_LIBRARY_PATH=/home/editorxu/ws/mjr/sdk/magic_humanoid_sdk/build:$LD_LIBRARY_PATH

## Example Execution

./high_level_motion_example

Reference to the high-level motion control state transitions described in the documentation:

1. Switch from suspended state to recovery stand
2. Switch from recovery stand state to balance stand
3. Execute trick actions in balance stand state
4. Send remote control commands to move forward in balance stand state
