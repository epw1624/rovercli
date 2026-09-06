cd "$ROVERFLAKE_ROOT"
rosdep update
rosdep install --from-paths src --ignore-src -r --skip-keys="serial moteus_msgs" -y --rosdistro $ROS_DISTRO