#!/bin/bash

# Install dependencies
sudo dnf install git cmake gcc-c++ \
	boost-devel eigen3-devel freeimage-devel \
	glew-devel glog-devel gflags-devel \
	qt5-qtbase-devel suitesparse-devel \
	openblas-devel cuda-toolkit \
	ceres-solver ceres-solver-devel \
	cgal-devel tbb-devel metis-devel

# Clone COLMAP
git clone https://github.com/colmap/colmap.git
cd colmap

# Build COLMAP
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release \
	-DGLOG_FOUND=ON \
	-DGLOG_INCLUDE_DIRS=/usr/include \
	-DGLOG_LIBRARIES=/usr/lib64/libglog.so

make -j$(nproc)
sudo make install

# Verify installation
colmap -h
