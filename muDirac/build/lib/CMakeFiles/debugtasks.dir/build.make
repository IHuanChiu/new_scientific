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
include lib/CMakeFiles/debugtasks.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include lib/CMakeFiles/debugtasks.dir/compiler_depend.make

# Include the progress variables for this target.
include lib/CMakeFiles/debugtasks.dir/progress.make

# Include the compile flags for this target's objects.
include lib/CMakeFiles/debugtasks.dir/flags.make

lib/CMakeFiles/debugtasks.dir/debugtasks.cpp.o: lib/CMakeFiles/debugtasks.dir/flags.make
lib/CMakeFiles/debugtasks.dir/debugtasks.cpp.o: ../lib/debugtasks.cpp
lib/CMakeFiles/debugtasks.dir/debugtasks.cpp.o: lib/CMakeFiles/debugtasks.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object lib/CMakeFiles/debugtasks.dir/debugtasks.cpp.o"
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/lib && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT lib/CMakeFiles/debugtasks.dir/debugtasks.cpp.o -MF CMakeFiles/debugtasks.dir/debugtasks.cpp.o.d -o CMakeFiles/debugtasks.dir/debugtasks.cpp.o -c /Users/chiu.i-huan/Desktop/new_scientific/mudirac/lib/debugtasks.cpp

lib/CMakeFiles/debugtasks.dir/debugtasks.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/debugtasks.dir/debugtasks.cpp.i"
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/lib && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/chiu.i-huan/Desktop/new_scientific/mudirac/lib/debugtasks.cpp > CMakeFiles/debugtasks.dir/debugtasks.cpp.i

lib/CMakeFiles/debugtasks.dir/debugtasks.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/debugtasks.dir/debugtasks.cpp.s"
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/lib && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/chiu.i-huan/Desktop/new_scientific/mudirac/lib/debugtasks.cpp -o CMakeFiles/debugtasks.dir/debugtasks.cpp.s

# Object files for target debugtasks
debugtasks_OBJECTS = \
"CMakeFiles/debugtasks.dir/debugtasks.cpp.o"

# External object files for target debugtasks
debugtasks_EXTERNAL_OBJECTS =

lib/libdebugtasks.a: lib/CMakeFiles/debugtasks.dir/debugtasks.cpp.o
lib/libdebugtasks.a: lib/CMakeFiles/debugtasks.dir/build.make
lib/libdebugtasks.a: lib/CMakeFiles/debugtasks.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library libdebugtasks.a"
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/lib && $(CMAKE_COMMAND) -P CMakeFiles/debugtasks.dir/cmake_clean_target.cmake
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/lib && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/debugtasks.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
lib/CMakeFiles/debugtasks.dir/build: lib/libdebugtasks.a
.PHONY : lib/CMakeFiles/debugtasks.dir/build

lib/CMakeFiles/debugtasks.dir/clean:
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/lib && $(CMAKE_COMMAND) -P CMakeFiles/debugtasks.dir/cmake_clean.cmake
.PHONY : lib/CMakeFiles/debugtasks.dir/clean

lib/CMakeFiles/debugtasks.dir/depend:
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/chiu.i-huan/Desktop/new_scientific/mudirac /Users/chiu.i-huan/Desktop/new_scientific/mudirac/lib /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/lib /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/lib/CMakeFiles/debugtasks.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : lib/CMakeFiles/debugtasks.dir/depend

