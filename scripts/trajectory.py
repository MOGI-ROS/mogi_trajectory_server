import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped

class TrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('trajectory_publisher')
        self.declare_parameter("trajectory_topic", "trajectory")
        self.declare_parameter("odometry_topic", "odom")
        self.path_pub = self.create_publisher(Path, self.get_parameter("trajectory_topic").value, 10)
        self.odom_sub = self.create_subscription(Odometry, self.get_parameter("odometry_topic").value, self.odom_callback, 10)
        
        self.path = Path()
        self.path.header.frame_id = "odom"

    def odom_callback(self, msg):
        # Create a PoseStamped message from the Odometry data
        pose = PoseStamped()
        pose.header = msg.header
        pose.pose = msg.pose.pose

        # Append the pose to the path
        self.path.header.stamp = msg.header.stamp
        self.path.poses.append(pose)

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