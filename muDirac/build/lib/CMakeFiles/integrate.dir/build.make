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
include lib/CMakeFiles/integrate.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include lib/CMakeFiles/integrate.dir/compiler_depend.make

# Include the progress variables for this target.
include lib/CMakeFiles/integrate.dir/progress.make

# Include the compile flags for this target's objects.
include lib/CMakeFiles/integrate.dir/flags.make

lib/CMakeFiles/integrate.dir/integrate.cpp.o: lib/CMakeFiles/integrate.dir/flags.make
lib/CMakeFiles/integrate.dir/integrate.cpp.o: /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/lib/integrate.cpp
lib/CMakeFiles/integrate.dir/integrate.cpp.o: lib/CMakeFiles/integrate.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object lib/CMakeFiles/integrate.dir/integrate.cpp.o"
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT lib/CMakeFiles/integrate.dir/integrate.cpp.o -MF CMakeFiles/integrate.dir/integrate.cpp.o.d -o CMakeFiles/integrate.dir/integrate.cpp.o -c /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/lib/integrate.cpp

lib/CMakeFiles/integrate.dir/integrate.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/integrate.dir/integrate.cpp.i"
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/lib/integrate.cpp > CMakeFiles/integrate.dir/integrate.cpp.i

lib/CMakeFiles/integrate.dir/integrate.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/integrate.dir/integrate.cpp.s"
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/lib/integrate.cpp -o CMakeFiles/integrate.dir/integrate.cpp.s

# Object files for target integrate
integrate_OBJECTS = \
"CMakeFiles/integrate.dir/integrate.cpp.o"

# External object files for target integrate
integrate_EXTERNAL_OBJECTS =

lib/libintegrate.a: lib/CMakeFiles/integrate.dir/integrate.cpp.o
lib/libintegrate.a: lib/CMakeFiles/integrate.dir/build.make
lib/libintegrate.a: lib/CMakeFiles/integrate.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library libintegrate.a"
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && $(CMAKE_COMMAND) -P CMakeFiles/integrate.dir/cmake_clean_target.cmake
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/integrate.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
lib/CMakeFiles/integrate.dir/build: lib/libintegrate.a
.PHONY : lib/CMakeFiles/integrate.dir/build

lib/CMakeFiles/integrate.dir/clean:
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib && $(CMAKE_COMMAND) -P CMakeFiles/integrate.dir/cmake_clean.cmake
.PHONY : lib/CMakeFiles/integrate.dir/clean

lib/CMakeFiles/integrate.dir/depend:
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/lib /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/lib/CMakeFiles/integrate.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : lib/CMakeFiles/integrate.dir/depend

