# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.20

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
CMAKE_COMMAND = /usr/local/Cellar/cmake/3.20.0/bin/cmake

# The command to remove a file.
RM = /usr/local/Cellar/cmake/3.20.0/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/chiu.i-huan/Desktop/new_scientific/mudirac

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build

# Include any dependencies generated for this target.
include lib/CMakeFiles/transforms.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include lib/CMakeFiles/transforms.dir/compiler_depend.make

# Include the progress variables for this target.
include lib/CMakeFiles/transforms.dir/progress.make

# Include the compile flags for this target's objects.
include lib/CMakeFiles/transforms.dir/flags.make

lib/CMakeFiles/transforms.dir/transforms.cpp.o: lib/CMakeFiles/transforms.dir/flags.make
lib/CMakeFiles/transforms.dir/transforms.cpp.o: ../lib/transforms.cpp
lib/CMakeFiles/transforms.dir/transforms.cpp.o: lib/CMakeFiles/transforms.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object lib/CMakeFiles/transforms.dir/transforms.cpp.o"
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/lib && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT lib/CMakeFiles/transforms.dir/transforms.cpp.o -MF CMakeFiles/transforms.dir/transforms.cpp.o.d -o CMakeFiles/transforms.dir/transforms.cpp.o -c /Users/chiu.i-huan/Desktop/new_scientific/mudirac/lib/transforms.cpp

lib/CMakeFiles/transforms.dir/transforms.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/transforms.dir/transforms.cpp.i"
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/lib && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/chiu.i-huan/Desktop/new_scientific/mudirac/lib/transforms.cpp > CMakeFiles/transforms.dir/transforms.cpp.i

lib/CMakeFiles/transforms.dir/transforms.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/transforms.dir/transforms.cpp.s"
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/lib && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/chiu.i-huan/Desktop/new_scientific/mudirac/lib/transforms.cpp -o CMakeFiles/transforms.dir/transforms.cpp.s

# Object files for target transforms
transforms_OBJECTS = \
"CMakeFiles/transforms.dir/transforms.cpp.o"

# External object files for target transforms
transforms_EXTERNAL_OBJECTS =

lib/libtransforms.a: lib/CMakeFiles/transforms.dir/transforms.cpp.o
lib/libtransforms.a: lib/CMakeFiles/transforms.dir/build.make
lib/libtransforms.a: lib/CMakeFiles/transforms.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library libtransforms.a"
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/lib && $(CMAKE_COMMAND) -P CMakeFiles/transforms.dir/cmake_clean_target.cmake
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/lib && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/transforms.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
lib/CMakeFiles/transforms.dir/build: lib/libtransforms.a
.PHONY : lib/CMakeFiles/transforms.dir/build

lib/CMakeFiles/transforms.dir/clean:
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/lib && $(CMAKE_COMMAND) -P CMakeFiles/transforms.dir/cmake_clean.cmake
.PHONY : lib/CMakeFiles/transforms.dir/clean

lib/CMakeFiles/transforms.dir/depend:
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/chiu.i-huan/Desktop/new_scientific/mudirac /Users/chiu.i-huan/Desktop/new_scientific/mudirac/lib /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/lib /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/lib/CMakeFiles/transforms.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : lib/CMakeFiles/transforms.dir/depend

