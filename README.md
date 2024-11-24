# mogi_trajectory_server
Trajectory visualization for ROS2

Pretty much the same as hector_trajectory_server for ROS1 to show robot's trajectory as a path in rviz.

Usage:
```bash
ros2 run mogi_trajectory_server mogi_trajectory_server
```

It has 2 configurable parameters:
```python
self.declare_parameter("trajectory_topic", "trajectory")
self.declare_parameter("odometry_topic", "odom")
```