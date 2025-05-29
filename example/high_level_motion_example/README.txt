# 示例说明

## 运行时依赖
export LD_LIBRARY_PATH=/home/editorxu/ws/mjr/sdk/magic_humanoid_sdk/build:$LD_LIBRARY_PATH

## 示例执行

参考文档中描述的高层运动控制的状态切换：

1. 从挂起状态切换到站立锁定
./recovery_stand_example

2. 从站立锁定状态切换到平衡站立
./balance_stand_example

3. 在平衡站立状态，执行特技动作
./execute_trick_action_example

4. 在平衡站立状态下，发送遥控指令向前行进
./joy_control_example
