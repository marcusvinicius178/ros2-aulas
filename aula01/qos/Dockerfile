FROM osrf/ros:foxy-desktop
 
RUN apt-get update \
 && apt-get install -y \
    wget \
    lsb-release \
    sudo \
    mesa-utils \
 && apt-get clean
 
# Get gazebo binaries
RUN echo "deb http://packages.osrfoundation.org/gazebo/ubuntu `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list \
 && wget http://packages.osrfoundation.org/gazebo.key -O - | apt-key add - \
 && apt-get update \
 && apt-get install -y \
    gazebo11 \
    ros-foxy-gazebo-ros-pkgs \
    ros-foxy-joy \
    libignition-math6 \
    libignition-math6-dev \
 && apt-get clean
 
RUN mkdir -p /tmp/workspace/src
COPY prius_description /tmp/workspace/src/prius_description
COPY prius_msgs /tmp/workspace/src/prius_msgs
COPY car_demo /tmp/workspace/src/car_demo
COPY qos_demo_visual /tmp/workspace/src/qos_demo_visual
 
# FIX: ament_python is not a rosdep-resolvable key; remove it from package.xml
RUN sed -i '/<buildtool_depend>ament_python<\/buildtool_depend>/d' /tmp/workspace/src/qos_demo_visual/package.xml
 
RUN /bin/bash -c 'cd /tmp/workspace \
 && source /opt/ros/foxy/setup.bash \
 && if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then rosdep init; fi \
 && rosdep update --include-eol-distros \
 && rosdep install -y --from-paths src --ignore-src --rosdistro foxy \
 && colcon build --symlink-install'
 
CMD ["/bin/bash", "-c", "source /opt/ros/foxy/setup.bash && source /tmp/workspace/install/setup.bash && ros2 launch car_demo demo.launch.py"]
 
