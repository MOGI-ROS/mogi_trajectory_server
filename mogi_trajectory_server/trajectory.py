import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped, TransformStamped
from tf2_ros import TransformListener, Buffer
import math

class TrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('trajectory_publisher')
        self.declare_parameter("trajectory_topic", "trajectory")
        self.declare_parameter("reference_frame_id", "odom")
        self.declare_parameter("robot_frame_id", "base_link")
        self.declare_parameter("update_rate", 3.0) # in Hz
        self.declare_parameter("publish_rate", 2.0) # in Hz
        self.declare_parameter("min_distance", 0.1) # in meters

        # TF2 Listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Default values
        self.update_rate = self.get_parameter("update_rate").value
        self.publish_rate = self.get_parameter("publish_rate").value
        self.min_distance = self.get_parameter("min_distance").value
        self.reference_frame_id = self.get_parameter("reference_frame_id").value
        self.robot_frame_id = self.get_parameter("robot_frame_id").value

        # Create seperate timers for publisher and transformation
        self.path_pub = self.create_publisher(Path, self.get_parameter("trajectory_topic").value, 10)
        self.publish_timer = self.create_timer(1.0/self.publish_rate, self.publish_trajectory)
        self.transform_timer = self.create_timer(1.0/self.update_rate, self.get_pose)
        
        # Trajectory message header is the same as target frame id
        self.last_pose = None
        self.path = Path()
        self.path.header.frame_id = self.get_parameter("reference_frame_id").value

    def get_pose(self):
        try:
            # Look up the transformation between reference frame and robot frame
            transform: TransformStamped = self.tf_buffer.lookup_transform(
                self.reference_frame_id,
                self.robot_frame_id,
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=1.0)
            )

            # Extract the position
            pose = PoseStamped()
            pose.header.stamp = transform.header.stamp
            pose.header.frame_id = self.reference_frame_id
            pose.pose.position.x = transform.transform.translation.x
            pose.pose.position.y = transform.transform.translation.y
            pose.pose.position.z = transform.transform.translation.z
            pose.pose.orientation = transform.transform.rotation

            # Append the first pose anyway to the path
            if self.last_pose == None:
                self.path.poses.append(pose)
                self.last_pose = pose
                return

            # Check the distance change in 2D
            distance_moved = math.sqrt((pose.pose.position.x - self.last_pose.pose.position.x)**2 + (pose.pose.position.y - self.last_pose.pose.position.y)**2)

            if distance_moved >= self.min_distance:
                # Append the pose to the path
                self.path.poses.append(pose)
                self.last_pose = pose

            return

        except Exception as e:
            self.get_logger().warn(f"Could not get transform: {e}")
            return

    def publish_trajectory(self):
        # Create timestamp for the header
        self.path.header.stamp = self.get_clock().now().to_msg()
        # Publish the path
        self.path_pub.publish(self.path)

def main(args=None):
    rclpy.init(args=args)
    trajectory_publisher = TrajectoryPublisher()
    rclpy.spin(trajectory_publisher)
    trajectory_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()