#!/bin/bash

LIBREALSENSE_DIRECTORY=${HOME}/librealsense
LIBREALSENSE_VERSION=v2.31.0
INSTALL_DIR=$PWD

red=`tput setaf 1`
green=`t2put setaf `
reset=`tput sgr0`

echo ""
echo "Please make sure that no RealSense cameras are currently attached"
echo ""
read -n 1 -s -r -p "Press any key to continue"
echo ""

if [ ! -d "$LIBREALSENSE_DIRECTORY" ] ; then
  # clone librealsense
  cd ${HOME}
  echo "${green}Cloning librealsense${reset}"
  git clone https://github.com/IntelRealSense/librealsense.git
fi

# Is the version of librealsense current enough?
cd $LIBREALSENSE_DIRECTORY
VERSION_TAG=$(git tag -l $LIBREALSENSE_VERSION)
if [ ! $VERSION_TAG  ] ; then
   echo ""
  tput setaf 1
  echo "==== librealsense Version Mismatch! ============="
  tput sgr0
  echo ""
  echo "The installed version of librealsense is not current enough for these scripts."
  echo "This script needs librealsense tag version: "$LIBREALSENSE_VERSION "but it is not available."
  echo "This script patches librealsense, the patches apply on the expected version."
  echo "Please upgrade librealsense before attempting to install again."
  echo ""
  exit 1
fi

# Checkout version the last tested version of librealsense
git checkout $LIBREALSENSE_VERSION

sudo apt-add-repository universe
sudo apt-get update
echo "${green}Adding dependencies, graphics libraries and tools${reset}"
sudo apt-get install libssl-dev libusb-1.0-0-dev pkg-config -y
# This is for ccmake
sudo apt-get install build-essential cmake cmake-curses-gui -y

# Graphics libraries - for SDK's OpenGL-enabled examples
sudo apt-get install libgtk-3-dev libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev -y

cd $LIBREALSENSE_DIRECTORY
git checkout $LIBREALSENSE_VERSION

# echo "${green}Applying Model-Views Patch${reset}"
# The render loop of the post processing does not yield; add a sleep
# patch -p1 -i $INSTALL_DIR/patches/model-views.patch

# echo "${green}Applying Incomplete Frames Patch${reset}"
# The Jetson tends to return incomplete frames at high frame rates; suppress error logging
# patch -p1 -i $INSTALL_DIR/patches/incomplete-frame.patch


echo "${green}Applying udev rules${reset}"
# Copy over the udev rules so that camera can be run from user space
sudo cp config/99-realsense-libusb.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && udevadm trigger

# Now compile librealsense and install
mkdir build 
cd build
# Build examples, including graphical ones
echo "${green}Configuring Make system${reset}"
# Use the CMake version that we built, must be > 3.8
# Build with CUDA (default), the CUDA flag is USE_CUDA, ie -DUSE_CUDA=true
cmake ../ -DBUILD_EXAMPLES=true -DCMAKE_BUILD_TYPE=Release -DBUILD_WITH_CUDA=ON -DFORCE_RSUSB_BACKEND:BOOL=ON -DBUILD_PYTHON_BINDINGS=true -DPYTHON_EXECUTABLE=`which python`
# The library will be installed in /usr/local/lib, header files in /usr/local/include
# The demos, tutorials and tests will located in /usr/local/bin.
echo "${green}Building librealsense, headers, tools and demos${reset}"

NUM_CPU=$(nproc)
time make -j$(($NUM_CPU - 1))
if [ $? -eq 0 ] ; then
  echo "librealsense make successful"
else
  echo "librealsense did not successfully build" >&2
  echo "Please fix issues and retry build"
  exit 1
fi
echo "${green}Installing librealsense, headers, tools and demos${reset}"
sudo make install
echo "${green}Library Installed${reset}"
echo " "
echo " -----------------------------------------"
echo "The library is installed in /usr/local/lib"
echo "The header files are in /usr/local/include"
echo "The demos and tools are located in /usr/local/bin"
echo " "
echo " -----------------------------------------"
echo " "


echo 'export PYTHONPATH=/usr/local/lib:$PYTHONPATH' >> ~/.bashrc
source ~/.bashrc

