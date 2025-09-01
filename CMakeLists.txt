cmake_minimum_required(VERSION 3.18)

project(magicbot_gen1_sdk LANGUAGES C CXX)

# Project Options
option(BUILD_EXAMPLES "Build examples" OFF)

# Set cmake path
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

# Some necessary settings
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Set default build type as Release
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

set(CMAKE_CXX_VISIBILITY_PRESET hidden)
set(CMAKE_CXX_VISIBILITY_INLINES_HIDDEN ON)
set(BUILD_SHARED_LIBS ON)

message(STATUS "Current system architecture: ${CMAKE_SYSTEM_PROCESSOR}")

set(MAGICBOT_GEN1_SDK_PATH
    ${CMAKE_CURRENT_SOURCE_DIR}/lib/${CMAKE_SYSTEM_PROCESSOR})
find_library(
  MAGICBOT_GEN1_SDK_LIB magicbot_gen1_sdk
  PATHS ${MAGICBOT_GEN1_SDK_PATH}
  NO_DEFAULT_PATH)

if(NOT MAGICBOT_GEN1_SDK_LIB)
  message(FATAL_ERROR "Magiclab SDK library for the architecture is not found")
else()
  message(STATUS "Magiclab SDK library found at: ${MAGICBOT_GEN1_SDK_LIB}")
endif()

message(STATUS "Importing: ${MAGICBOT_GEN1_SDK_LIB}")

# Python SDK module path
set(MAGICBOT_GEN1_PYTHON_SDK_PATH
    ${CMAKE_CURRENT_SOURCE_DIR}/lib/${CMAKE_SYSTEM_PROCESSOR})

# Determine Python module filename based on architecture
if(CMAKE_SYSTEM_PROCESSOR STREQUAL "x86_64")
  set(PYTHON_MODULE_NAME "magicbot_gen1_python.cpython-310-x86_64-linux-gnu.so")
elseif(CMAKE_SYSTEM_PROCESSOR STREQUAL "aarch64")
  set(PYTHON_MODULE_NAME
      "magicbot_gen1_python.cpython-310-aarch64-linux-gnu.so")
else()
  message(FATAL_ERROR "Unsupported architecture: ${CMAKE_SYSTEM_PROCESSOR}")
endif()

set(MAGICBOT_GEN1_PYTHON_SDK_LIB
    ${MAGICBOT_GEN1_PYTHON_SDK_PATH}/${PYTHON_MODULE_NAME})

if(NOT EXISTS ${MAGICBOT_GEN1_PYTHON_SDK_LIB})
  message(
    FATAL_ERROR
      "Magiclab Python SDK module for the architecture is not found: ${MAGICBOT_GEN1_PYTHON_SDK_LIB}"
  )
else()
  message(
    STATUS
      "Magiclab Python SDK module found at: ${MAGICBOT_GEN1_PYTHON_SDK_LIB}")
endif()

message(STATUS "Importing: ${MAGICBOT_GEN1_PYTHON_SDK_LIB}")

add_library(magicbot_gen1_sdk SHARED IMPORTED GLOBAL)
add_library(magicbot_gen1::sdk ALIAS magicbot_gen1_sdk)

set_target_properties(magicbot_gen1_sdk PROPERTIES IMPORTED_LOCATION
                                                   ${MAGICBOT_GEN1_SDK_LIB})
target_include_directories(
  magicbot_gen1_sdk
  INTERFACE $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
            $<INSTALL_INTERFACE:include>)

# build examples
if(BUILD_EXAMPLES)
  add_subdirectory(example/cpp)
endif()

include(GNUInstallDirs)

install(FILES cmake/magicbot_gen1_sdkTargets.cmake
        DESTINATION lib/cmake/magicbot_gen1_sdk)
install(FILES ${MAGICBOT_GEN1_SDK_LIB} DESTINATION ${CMAKE_INSTALL_LIBDIR})
install(FILES ${MAGICBOT_GEN1_PYTHON_SDK_LIB}
        DESTINATION ${CMAKE_INSTALL_LIBDIR})
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

include(CMakePackageConfigHelpers)
write_basic_package_version_file(
  magicbot_gen1_sdkConfigVersion.cmake
  VERSION
    "${${PROJECT_NAME}_VERSION_MAJOR}.${${PROJECT_NAME}_VERSION_MINOR}.${${PROJECT_NAME}_VERSION_PATCH}"
  COMPATIBILITY ExactVersion)

configure_file(cmake/magicbot_gen1_sdkConfig.cmake.in
               magicbot_gen1_sdkConfig.cmake @ONLY)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/magicbot_gen1_sdkConfig.cmake"
              "${CMAKE_CURRENT_BINARY_DIR}/magicbot_gen1_sdkConfigVersion.cmake"
        DESTINATION lib/cmake/magicbot_gen1_sdk)
