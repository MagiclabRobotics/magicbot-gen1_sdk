# magicbot-gen1_sdk


## SDK Environment Requirements


This SDK requires the following software and hardware environment to function properly. Please ensure all dependencies are installed and configured before using the SDK.

### 1. Operating System

- Ubuntu 22.04 or later (recommended)  

#### System Configuration

The following configurations need to be added to the `/etc/security/limits.conf` file for regular users:

```
*    -   rtprio   98
```

### 2. Compiler & Toolchain

- GCC version ≥ 11.4 (for Linux)
- CMake ≥ 3.18
- Make build system

### 3. Programming Language

- C++20 (minimum)

### 4. Required Dependencies

You must install the following libraries/packages before building or using the SDK.

#### System Libraries

- `libspdlog-dev`
- `libyaml-cpp-dev`
- `liblcm-dev`

Shell command:
```Bash
sudo apt install -y libspdlog-dev libyaml-cpp-dev liblcm-dev
```

## Build examples
To build the examples inside this reposity:
```
  sh build.sh
```

## Doc
Installing Sphinx dependencies:
```
  pip install sphinx
  pip install myst-parser
  pip install linkify-it-py
```
Build Sphinx documentation：
```
  cd doc/
  make html
```
Enter doc/build/html directory, and open `index.html`


## Installation

To build your own application with this SDK, you can install the magic_gen1_sdk to specified directory:
```
  mkdir build
  cd build
  cmake .. -DCMAKE_INSTALL_PREFIX=/opt/magic_robotics/magic_gen1_sdk
  make -j8
  sudo make install
```
You can refer to example/cmake_sample on how to import the `magic_gen1_sdk` into your CMake project.
```
  cd example/cmake_example
  mkdir build
  cd build
  cmake .. -DCMAKE_PREFIX_PATH=/opt/magic_robotics/magic_gen1_sdk
  make -j8
```
Note that the path specified by -DCMAKE_PREFIX_PATH must be the same as the installation directory used above.

## Notice

For more reference information, please go to [MagicRobotics](https://github.com/MagiclabRobotics)

