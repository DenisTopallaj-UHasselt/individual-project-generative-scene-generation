#!/bin/bash

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
