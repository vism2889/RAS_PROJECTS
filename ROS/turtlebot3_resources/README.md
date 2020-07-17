# Turtlebot3 with Ubuntu 18.04 and ROS Melodic

### These instructions assume you already on a system running Ubuntu 18.04 have ROS Melodic installed.

##### You will need to go into the catkin workspace you want to build turtlebot3 in.
`cd ~/turtlebot3_catkin_ws/src`

##### If you wish to make a new workspace:
`mkdir turtlebot3_catkin_ws`

`catkin_build`

`cd ~/src`

##### Now make sure you're in the `~/src` folder and download the Turtlebot3 requirements via the following commands:
`git clone https://github.com/ROBOTIS-GIT/turtlebot3.git`

`git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git`

`git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git`

`git clone https://github.com/ROBOTIS-GIT/turtlebot3_applications.git`

`git clone https://github.com/ROBOTIS-GIT/turtlebot3_autorace.git`

`git clone https://github.com/ROBOTIS-GIT/turtlebot3_deliver.git`

`git clone https://github.com/ROBOTIS-GIT/turtlebot3_description.git`

`git clone https://github.com/ROBOTIS-GIT/turtlebot3_gazebo.git`

`git clone https://github.com/ROBOTIS-GIT/hls_lfcd_lds_driver.git`

`git clone https://github.com/ROBOTIS-GIT/open_manipulator.git`

`git clone https://github.com/ROBOTIS-GIT/Dynamixel_SDK.git`

`git clone https://github.com/ROBOTIS-GIT/Dynamixel-workbench.git`

`git clone https://github.com/ROBOTIS-GIT/dynamixel-workbench-msgs.git`

`git clone https://github.com/ROBOTIS-GIT/open_manipulator.git`

`git clone https://github.com/ROBOTIS-GIT/open_manipulator_dependencies.git`

`git clone https://github.com/ROBOTIS-GIT/open_manipulator_msgs.git`

`git clone https://github.com/ROBOTIS-GIT/open_manipulator_simulations.git`

`git clone https://github.com/ROBOTIS-GIT/robotis_manipulator.git`

`git clone https://github.com/ROBOTIS-GIT/OpenCR.git`

##### Once all of the requirements above have been installed we can build our catkin workspace:
`cd ~/turtlebot3_catkin_ws`

`catkin_make`


##### Source your catkin workspace and configure turtlebot3 model :
###### (do this in every terminal window you plan on running rostopics or turtlebot3 commands from)
`source ./devel/setup.bash`

`export TURTLEBOT3_MODEL=burger`

##### Test your workspace:
##### In a new terminal window: (Start ROSCORE)
`roscore`

##### In another new terminal window: (Start Gazebo)
`cd ~/turtlebot3_catkin_ws`

`source ./devel/setup.bash`

`export TURTLEBOT3_MODEL=burger`

`roslaunch turtlebot3_gazebo turtlebot3_world.launch`

##### In another new terminal window: (Start teleop to use keyboard keys as controls, *This window must be selected for controls to work*)
`cd ~/turtlebot3_catkin_ws`

`source ./devel/setup.bash`

`export TURTLEBOT3_MODEL=burger`

`roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch`

##### In another new terminal window: (Starts RVIZ to visualize sensor data)
`cd ~/turtlebot3_catkin_ws`

`source ./devel/setup.bash`

`export TURTLEBOT3_MODEL=burger`

`roslaunch turtlebot3_gazebo turtlebot3_gazebo_rviz.launch`
