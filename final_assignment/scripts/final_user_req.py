#! /usr/bin/env python
# importing ros dependencies
import rospy
from std_srvs.srv import *
import time
from time import sleep
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseActionGoal
from actionlib_msgs.msg import GoalStatusArray
from my_srv.srv import Finalassignment

target_reached_status = 0



def clbk_move_base_status(msg):
    """This function is called when status from move_base is received"""
    global target_reached_status
    if (len(msg.status_list) > 0):
        if msg.status_list[0].status == 3:
	    target_reached_status = 1


def main():
    """This code enables get the user request, and let the robot execute on one of the previously defined behaviors (depending on the input of user)."""

    """Here ROS node is initialized"""
    rospy.init_node('final_user_req')

    global target_reached_status, wall_follower_client

    """ Initializing client for random target index service """
    random_index_service = rospy.ServiceProxy('/finalassignment', Finalassignment)

    """ Initializing subscriber to topic /move_base/status """
    move_base_status = rospy.Subscriber('/move_base/status', GoalStatusArray, clbk_move_base_status, queue_size = 1)

    """ Initializing publisher for new target on topic move_base/goal """
    new_target_pub = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size = 1)

    """ Initializing client for wall follower service """
    wall_follower_client = rospy.ServiceProxy('/wall_follower_switch', SetBool)

    """ Initializing publisher on topic /cmd_vel """
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)

    """ List of 6 possible target coordinates """
    random_targets = [(-4,-3), (-4,2), (-4,7), (5,-7), (5,-3), (5,1)]

    print("\nInitializing...\n")
    
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():

        print("""\nEnter integers from 1 to 4 to execute the following behaviors:
(1) Move randomly in the environment, by choosing 1 out of 6 possible target positions.
(2) Enter the next target position out of the possible six and reach it.
(3) Start following the external walls.
(4) Stop in the last position.""")


	""" User input for states from 1 to 4 """
        x = int(raw_input("\nEnter a number from 1 to 4 corresponding to the chosen robot behavior: "))

	
	if (x == 1):
	    """ Move randomly the robot in the environment, by choosing 1 out of 6 possible target positions """


	    """ Set flag of wall follower to False """
	    resp = wall_follower_client(False)

	    """ calling service to generate random index for target """
	    resp = random_index_service(1,6)
            rand_index = resp.target_index

            print("\nNew Target: (" + str(random_targets[rand_index -1][0]) + ", " + str(random_targets[rand_index -1][1]) + ")")

	    """ Send target (x,y) position to move_base """
	    MoveBase_msg = MoveBaseActionGoal()
	    MoveBase_msg.goal.target_pose.header.frame_id = "map"
	    MoveBase_msg.goal.target_pose.pose.orientation.w = 1
	    MoveBase_msg.goal.target_pose.pose.position.x = random_targets[rand_index -1][0]
	    MoveBase_msg.goal.target_pose.pose.position.y = random_targets[rand_index -1][1]
	    new_target_pub.publish(MoveBase_msg)

	    print('\nRobot is moving towards the target position.')
	    sleep(15)
            target_reached_status = 0

            """ Condition to see if the robot has reached the target """
	    while(target_reached_status == 0):
                sleep(1)
            print('\nRobot reached the target position.')


	
        elif (x == 2):
	    """  ask the user for the next target position ,checking that the position is one of the possible six and reach it """
        
	    """ Set flag of wall follower to False """
	    resp = wall_follower_client(False)

	    print("""\nTarget coordinates:
1. (-4,-3)
2. (-4,2)
3. (-4,7) 
4. (5,-7)
5. (5,-3)
6. (5,1)""")

	    user_input = int(raw_input("\nEnter the number corresponding to the desired target coordinates: "))
            print("\nThe new target position is ("+ str(random_targets[user_input-1][0]) + ", " + str(random_targets[user_input-1][1]) + ")")

	    
	    """ Set and publish values of x, y, frame_id and w to move_base """
	    MoveBase_msg = MoveBaseActionGoal()
	    MoveBase_msg.goal.target_pose.header.frame_id = "map"
	    MoveBase_msg.goal.target_pose.pose.orientation.w = 1
	    MoveBase_msg.goal.target_pose.pose.position.x = random_targets[user_input-1][0]
	    MoveBase_msg.goal.target_pose.pose.position.y = random_targets[user_input-1][1]
	    new_target_pub.publish(MoveBase_msg)

	    print('\nRobot is moving towards the target position.')
	    sleep(15)
	    target_reached_status = 0

            """ Condition to see if the robot has reached the target """
	    while(target_reached_status == 0):
	        sleep(1)
            print('\nRobot has reached the target position.')

	
	elif (x == 3):
	    """ Start following the external walls """

    
            """ Set flag of wall follower to True """
            resp = wall_follower_client(True)
            print('\nRobot is demonstrating wall-following behavior.')

	
        elif (x == 4):
	    """ Stop in the last position. """

            """ Set the flag of wall follower to False """
            resp = wall_follower_client(False)

	    """ Set velocity of robot to zero and publish it """
            twist_msg = Twist()
            twist_msg.linear.x = 0
            twist_msg.angular.z = 0
            pub.publish(twist_msg)
            print('\nRobot has stopped.')

	else:
	    continue
	
        rate.sleep()


if __name__ == '__main__':
    main()
