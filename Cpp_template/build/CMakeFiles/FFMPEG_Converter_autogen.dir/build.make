# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.27

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /opt/homebrew/Cellar/cmake/3.27.6/bin/cmake

# The command to remove a file.
RM = /opt/homebrew/Cellar/cmake/3.27.6/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/james/Documents/Development/University/AudioVideoEncoding/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/james/Documents/Development/University/AudioVideoEncoding/build

# Utility rule file for FFMPEG_Converter_autogen.

# Include any custom commands dependencies for this target.
include CMakeFiles/FFMPEG_Converter_autogen.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/FFMPEG_Converter_autogen.dir/progress.make

CMakeFiles/FFMPEG_Converter_autogen:
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --blue --bold --progress-dir=/Users/james/Documents/Development/University/AudioVideoEncoding/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Automatic MOC and UIC for target FFMPEG_Converter"
	/opt/homebrew/Cellar/cmake/3.27.6/bin/cmake -E cmake_autogen /Users/james/Documents/Development/University/AudioVideoEncoding/build/CMakeFiles/FFMPEG_Converter_autogen.dir/AutogenInfo.json Debug

FFMPEG_Converter_autogen: CMakeFiles/FFMPEG_Converter_autogen
FFMPEG_Converter_autogen: CMakeFiles/FFMPEG_Converter_autogen.dir/build.make
.PHONY : FFMPEG_Converter_autogen

# Rule to build all files generated by this target.
CMakeFiles/FFMPEG_Converter_autogen.dir/build: FFMPEG_Converter_autogen
.PHONY : CMakeFiles/FFMPEG_Converter_autogen.dir/build

CMakeFiles/FFMPEG_Converter_autogen.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/FFMPEG_Converter_autogen.dir/cmake_clean.cmake
.PHONY : CMakeFiles/FFMPEG_Converter_autogen.dir/clean

CMakeFiles/FFMPEG_Converter_autogen.dir/depend:
	cd /Users/james/Documents/Development/University/AudioVideoEncoding/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/james/Documents/Development/University/AudioVideoEncoding/src /Users/james/Documents/Development/University/AudioVideoEncoding/src /Users/james/Documents/Development/University/AudioVideoEncoding/build /Users/james/Documents/Development/University/AudioVideoEncoding/build /Users/james/Documents/Development/University/AudioVideoEncoding/build/CMakeFiles/FFMPEG_Converter_autogen.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/FFMPEG_Converter_autogen.dir/depend
