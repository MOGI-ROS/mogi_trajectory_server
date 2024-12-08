# mogi_trajectory_server
Trajectory visualization for ROS2 with pretty much the same functionality as `hector_trajectory_server` for ROS1.
This package provides a node that saves trajectory data based on the `odometry_topic` topic, the trajectory is saved internally as a `nav_msgs/Path` and can be obtained through the `trajectory_topic` topic.
The `publish_rate` and `min_distance` - that triggers an update - can be modified by parameters as described below.

## Usage:

Starting it as a node:
```bash
ros2 run mogi_trajectory_server mogi_trajectory_server
```

or within your launch file:

```python
trajectory_node = Node(
    package='mogi_trajectory_server',
    executable='mogi_trajectory_server',
    name='mogi_trajectory_server',
    parameters=[{'frame_id': 'odom'},
                {'odometry_topic': 'odom'}]
)
```

## Subscribed Topics:
```
odom (nav_msgs/Odometry)
```

## Published Topics:
```
trajectory (nav_msgs/Path)
```

## Parameters:

~`odometry_topic` (string, default: "odom")  
*The name of the odometry topic that the node subscribes*

~`trajectory_topic` (string, default: "trajectory")  
*The name of the published trajectory topic*

~`frame_id` (string, default: "odom")  
*The name of the target frame in the published message's header*

~`min_distance` (double, default: 0.1)  
*The minimum movement of the robot that triggers an update within the node*

~`publish_rate` (double, default: 2.0)  
*The publish rate in Hz for the trajectory published on the `trajectory` topic.*

