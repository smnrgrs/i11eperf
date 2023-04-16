#!/bin/bash


export CycloneDDS_DIR=/dds
mkdir build

cmake -B build/ -DDATATYPE=ou -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
cmake --build build/ -j8

