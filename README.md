[//]: # (Image References)

[image1]: ./trajectory.png "trajectory"

# mogi_trajectory_server
Trajectory visualization for ROS2 with pretty much the same functionality as `hector_trajectory_server` for ROS1.
This package provides a node that saves trajectory data using a TransformListener between `reference_frame_id` and `robot_frame_id`, the trajectory is saved internally as a `nav_msgs/Path` and can be obtained through the `trajectory_topic` topic.
The `update_rate`, `publish_rate` and `min_distance` - that triggers an update - can be modified by parameters as described below.

![alt text][image1]

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
    parameters=[{'reference_frame_id': 'map'},
                {'robot_frame_id': 'base_link'}]
)
```

## Subscribed Topics:
No topic subscription is needed because the node uses a TransformListener.

## Published Topics:
```
trajectory (nav_msgs/Path)
```

## Parameters:

~`trajectory_topic` (string, default: "trajectory")  
*The name of the published trajectory topic*

~`reference_frame_id` (string, default: "odom")  
*The name of the tf target frame, change it to map if your fixed frame is a map. It is also used in the published trajectory message's header*

~`robot_frame_id` (string, default: "base_link")  
*The name of the tf source frame = robot chassis frame*

~`update_rate` (double, default: 3.0)  
*The update rate in Hz for the trajectory update interanally using tf and TransformListener*

~`publish_rate` (double, default: 2.0)  
*The publish rate in Hz for the trajectory published on the `trajectory` topic*

~`min_distance` (double, default: 0.1)  
*The minimum movement of the robot that triggers an update within the node*



---
---
---

# mogi_trajectory_server_topic_based
Pretty much identical functiuonality but uses an odometry topic as input instead of TransformListener. It's not accurate on maps and in general not recommended to use over the `mogi_trajectory_server` but can be still useful in certain use cases.
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