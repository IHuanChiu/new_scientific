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
include lib/CMakeFiles/econfigs.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include lib/CMakeFiles/econfigs.dir/compiler_depend.make

# Include the progress variables for this target.
include lib/CMakeFiles/econfigs.dir/progress.make

# Include the compile flags for this target's objects.
include lib/CMakeFiles/econfigs.dir/flags.make

lib/CMakeFiles/econfigs.dir/econfigs.cpp.o: lib/CMakeFiles/econfigs.dir/flags.make
lib/CMakeFiles/econfigs.dir/econfigs.cpp.o: /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/lib/econfigs.cpp
lib/CMakeFiles/econfigs.dir/econfigs.cpp.o: lib/CMakeFiles/econfigs.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object lib/CMakeFiles/econfigs.dir/econfigs.cpp.o"
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT lib/CMakeFiles/econfigs.dir/econfigs.cpp.o -MF CMakeFiles/econfigs.dir/econfigs.cpp.o.d -o CMakeFiles/econfigs.dir/econfigs.cpp.o -c /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/lib/econfigs.cpp

lib/CMakeFiles/econfigs.dir/econfigs.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/econfigs.dir/econfigs.cpp.i"
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/lib/econfigs.cpp > CMakeFiles/econfigs.dir/econfigs.cpp.i

lib/CMakeFiles/econfigs.dir/econfigs.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/econfigs.dir/econfigs.cpp.s"
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/lib/econfigs.cpp -o CMakeFiles/econfigs.dir/econfigs.cpp.s

# Object files for target econfigs
econfigs_OBJECTS = \
"CMakeFiles/econfigs.dir/econfigs.cpp.o"

# External object files for target econfigs
econfigs_EXTERNAL_OBJECTS =

lib/libeconfigs.a: lib/CMakeFiles/econfigs.dir/econfigs.cpp.o
lib/libeconfigs.a: lib/CMakeFiles/econfigs.dir/build.make
lib/libeconfigs.a: lib/CMakeFiles/econfigs.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library libeconfigs.a"
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && $(CMAKE_COMMAND) -P CMakeFiles/econfigs.dir/cmake_clean_target.cmake
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/econfigs.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
lib/CMakeFiles/econfigs.dir/build: lib/libeconfigs.a
.PHONY : lib/CMakeFiles/econfigs.dir/build

lib/CMakeFiles/econfigs.dir/clean:
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && $(CMAKE_COMMAND) -P CMakeFiles/econfigs.dir/cmake_clean.cmake
.PHONY : lib/CMakeFiles/econfigs.dir/clean

lib/CMakeFiles/econfigs.dir/depend:
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/lib /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib/CMakeFiles/econfigs.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : lib/CMakeFiles/econfigs.dir/depend

