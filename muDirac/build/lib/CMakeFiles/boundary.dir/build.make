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
CMAKE_SOURCE_DIR = /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build

# Include any dependencies generated for this target.
include lib/CMakeFiles/boundary.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include lib/CMakeFiles/boundary.dir/compiler_depend.make

# Include the progress variables for this target.
include lib/CMakeFiles/boundary.dir/progress.make

# Include the compile flags for this target's objects.
include lib/CMakeFiles/boundary.dir/flags.make

lib/CMakeFiles/boundary.dir/boundary.cpp.o: lib/CMakeFiles/boundary.dir/flags.make
lib/CMakeFiles/boundary.dir/boundary.cpp.o: /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/lib/boundary.cpp
lib/CMakeFiles/boundary.dir/boundary.cpp.o: lib/CMakeFiles/boundary.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object lib/CMakeFiles/boundary.dir/boundary.cpp.o"
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT lib/CMakeFiles/boundary.dir/boundary.cpp.o -MF CMakeFiles/boundary.dir/boundary.cpp.o.d -o CMakeFiles/boundary.dir/boundary.cpp.o -c /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/lib/boundary.cpp

lib/CMakeFiles/boundary.dir/boundary.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/boundary.dir/boundary.cpp.i"
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/lib/boundary.cpp > CMakeFiles/boundary.dir/boundary.cpp.i

lib/CMakeFiles/boundary.dir/boundary.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/boundary.dir/boundary.cpp.s"
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/lib/boundary.cpp -o CMakeFiles/boundary.dir/boundary.cpp.s

# Object files for target boundary
boundary_OBJECTS = \
"CMakeFiles/boundary.dir/boundary.cpp.o"

# External object files for target boundary
boundary_EXTERNAL_OBJECTS =

lib/libboundary.a: lib/CMakeFiles/boundary.dir/boundary.cpp.o
lib/libboundary.a: lib/CMakeFiles/boundary.dir/build.make
lib/libboundary.a: lib/CMakeFiles/boundary.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library libboundary.a"
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && $(CMAKE_COMMAND) -P CMakeFiles/boundary.dir/cmake_clean_target.cmake
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/boundary.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
lib/CMakeFiles/boundary.dir/build: lib/libboundary.a
.PHONY : lib/CMakeFiles/boundary.dir/build

lib/CMakeFiles/boundary.dir/clean:
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && $(CMAKE_COMMAND) -P CMakeFiles/boundary.dir/cmake_clean.cmake
.PHONY : lib/CMakeFiles/boundary.dir/clean

lib/CMakeFiles/boundary.dir/depend:
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/lib /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib/CMakeFiles/boundary.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : lib/CMakeFiles/boundary.dir/depend

