cmake_minimum_required(VERSION 3.16)

project(FFMPEG_Converter)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -Wall")
set(CMAKE_BUILD_TYPE Debug)

# Set the path to Qt installation on macOS, including lib/cmake/Qt6
set(CMAKE_PREFIX_PATH "/Users/james/Qt/6.6.1/macos/lib/cmake")

find_package(Qt6 REQUIRED COMPONENTS Widgets)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

qt_add_executable(FFMPEG_Converter
    main.cpp
    CustomComponent.cpp
    CustomComponent.h
    MainWindow.cpp
    MainWindow.h
)

target_link_libraries(FFMPEG_Converter PRIVATE Qt6::Widgets)