import rclpy
from rclpy.node import Node
import numpy as np
from geometry_msgs.msg import Twist

class UGVController(Node):

    def __init__(self):
        super().__init__('ugv_controller')

        self.publisher = self.create_publisher(
            Twist,
            '/model/ugv/cmd_vel',
            10
        )

        # Hidden context
        self.context = np.random.choice([0,1])

        if self.context == 0:
            self.goal = np.array([5.0, 0.0])
        else:
            self.goal = np.array([0.0, 5.0])

        self.position = np.array([0.0, 0.0])
        self.timer = self.create_timer(0.1, self.move)

        self.get_logger().info(f"Hidden context = {self.context}")

    def move(self):
        direction = self.goal - self.position
        direction = direction / (np.linalg.norm(direction) + 1e-6)

        msg = Twist()
        msg.linear.x = 0.5 * direction[0]
        msg.linear.y = 0.5 * direction[1]

        self.publisher.publish(msg)

def main():
    rclpy.init()
    node = UGVController()
    rclpy.spin(node)