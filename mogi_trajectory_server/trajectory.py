import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped
import math

class TrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('trajectory_publisher')
        self.declare_parameter("trajectory_topic", "trajectory")
        self.declare_parameter("odometry_topic", "odom")
        self.declare_parameter("frame_id", "odom")
        self.declare_parameter("publish_rate", 2.0) # in Hz
        self.declare_parameter("min_distance", 0.1) # in meters

        self.publish_rate = self.get_parameter("publish_rate").value
        self.min_distance = self.get_parameter("min_distance").value

        self.path_pub = self.create_publisher(Path, self.get_parameter("trajectory_topic").value, 10)
        self.odom_sub = self.create_subscription(Odometry, self.get_parameter("odometry_topic").value, self.odom_callback, 10)
        self.timer = self.create_timer(1.0/self.publish_rate, self.publish_trajectory)
        
        self.last_pose = None
        self.path = Path()
        self.path.header.frame_id = self.get_parameter("frame_id").value

    def odom_callback(self, msg):
        # Create a PoseStamped message from the Odometry data
        pose = PoseStamped()
        pose.header = msg.header
        pose.pose = msg.pose.pose

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