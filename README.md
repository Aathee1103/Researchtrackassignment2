# Researchtrackassignment2
# Done by Aatheethyaa Dhanasekaran(Matiocola No.:S5051520)

# Descrption of the Assignmnet:
The assignment is done in a ROS architecture for controling a mobile robot in the Gazebo environment.The software relies on the move_base and gmapping packages for localizing the robot and plan its motion. The program acquires the user's request, and lets the robot execute one of the pre-defined behaviors accordingly, along with Simulataneous Localization and Mapping(SLAM),path planning and collision avoidance.

The program requests user input on the following states:
1.Robot moves randomly in the environment, by choosing 1 out of 6 possible target positions: [(-4,-3);(-4,2);(-4,7);(5,-7);(5,-3);(5,1)].
2.Program asks the user for the next target position, checking that the position is one of the possible six target positions, and the robot reaches it.
3.Robot starts following the external walls.
4.Robot stops in the last position.
{If the robot is in state 1 or 2, the system waits until the robot reaches the position in order to switch to state 3 or 4}.

The controller package final_assignment contains the scripts, launch files and other dependencies used to simulate the 3D environment and move the robot in it. The simulation_gmapping.launch file launches the house.world file environment. The main node final_ui.py contains the entire control structure for the mobile robot simulation.

For the first state, final_ui.py node requests my_srv for a random target position between the range of 1 to 6. Then, the main node publishes the target positions to /move_base/goal and check thes the status of goal by subscribing to the topic /move_base/status. When the robot reaches the target and the status displays it in the node, the main node requests the user to input again.
For the second state, the user chooses one out of six possible target positions (as before) and publishes it to /move_base/goal.
For the third state, the wall_follower service is utilized through initialization of a service client to allow the robot to follow the walls. The interface also allows the user to enter the same or different request at any point in this state.
For the fourth state, the node stops all actions and stops the robot by publishing commands of zero velocity in topic /cmd_vel. Same as in state 3, the interface allows the user to enter the same or different request at any point in this state.



The server package my_srv contains the C++ file final_server.cpp which contains the source code for generating random integer within a specified range and advertising it over the node /final. It uses a custom message which requests two integers namely min and max, and returns one random integer target_index within this range in response.

The following steps will run the simulator along with the controller nodes.

Gazebo is the 3D simulator while rviz is the 3D visualization tool for ROS. In the command line, launch Gazebo and rviz by executing the following command:
roslaunch final_assignment simulation_gmapping.launch
In a new command line tab, run the following command:
roslaunch final_assignment move_base.launch
In a new command line tab, run the following command:
rosrun final_assignment wall_follow_service_m.py
In a new command line tab, run the following command:
rosrun my_srv final_server
In a new command line tab, run the following command:
rosrun final_assignment final_ui.py
The information getting published in the topics can be printed on the command line using the 'echo' command. Run the following command:
rostopic echo /move_base/status
To display a graph of what's going on in the system, run the following command in a new command line tab:
rosrun rqt_graph rqt_graph
