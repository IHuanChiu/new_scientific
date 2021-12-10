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
include test/CMakeFiles/test_wavefunction.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include test/CMakeFiles/test_wavefunction.dir/compiler_depend.make

# Include the progress variables for this target.
include test/CMakeFiles/test_wavefunction.dir/progress.make

# Include the compile flags for this target's objects.
include test/CMakeFiles/test_wavefunction.dir/flags.make

test/CMakeFiles/test_wavefunction.dir/test_wavefunction.cpp.o: test/CMakeFiles/test_wavefunction.dir/flags.make
test/CMakeFiles/test_wavefunction.dir/test_wavefunction.cpp.o: ../test/test_wavefunction.cpp
test/CMakeFiles/test_wavefunction.dir/test_wavefunction.cpp.o: test/CMakeFiles/test_wavefunction.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object test/CMakeFiles/test_wavefunction.dir/test_wavefunction.cpp.o"
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/test && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT test/CMakeFiles/test_wavefunction.dir/test_wavefunction.cpp.o -MF CMakeFiles/test_wavefunction.dir/test_wavefunction.cpp.o.d -o CMakeFiles/test_wavefunction.dir/test_wavefunction.cpp.o -c /Users/chiu.i-huan/Desktop/new_scientific/mudirac/test/test_wavefunction.cpp

test/CMakeFiles/test_wavefunction.dir/test_wavefunction.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/test_wavefunction.dir/test_wavefunction.cpp.i"
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/test && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/chiu.i-huan/Desktop/new_scientific/mudirac/test/test_wavefunction.cpp > CMakeFiles/test_wavefunction.dir/test_wavefunction.cpp.i

test/CMakeFiles/test_wavefunction.dir/test_wavefunction.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/test_wavefunction.dir/test_wavefunction.cpp.s"
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/test && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/chiu.i-huan/Desktop/new_scientific/mudirac/test/test_wavefunction.cpp -o CMakeFiles/test_wavefunction.dir/test_wavefunction.cpp.s

# Object files for target test_wavefunction
test_wavefunction_OBJECTS = \
"CMakeFiles/test_wavefunction.dir/test_wavefunction.cpp.o"

# External object files for target test_wavefunction
test_wavefunction_EXTERNAL_OBJECTS =

test/test_wavefunction: test/CMakeFiles/test_wavefunction.dir/test_wavefunction.cpp.o
test/test_wavefunction: test/CMakeFiles/test_wavefunction.dir/build.make
test/test_wavefunction: test/libtest_main.a
test/test_wavefunction: lib/libdebugtasks.a
test/test_wavefunction: lib/libconfig.a
test/test_wavefunction: lib/liboutput.a
test/test_wavefunction: lib/libatom.a
test/test_wavefunction: lib/libboundary.a
test/test_wavefunction: lib/libstate.a
test/test_wavefunction: lib/libpotential.a
test/test_wavefunction: lib/libeconfigs.a
test/test_wavefunction: lib/libhydrogenic.a
test/test_wavefunction: lib/libtransforms.a
test/test_wavefunction: lib/libwavefunction.a
test/test_wavefunction: lib/libintegrate.a
test/test_wavefunction: lib/libelements.a
test/test_wavefunction: lib/libinput.a
test/test_wavefunction: lib/libutils.a
test/test_wavefunction: test/CMakeFiles/test_wavefunction.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable test_wavefunction"
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/test_wavefunction.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
test/CMakeFiles/test_wavefunction.dir/build: test/test_wavefunction
.PHONY : test/CMakeFiles/test_wavefunction.dir/build

test/CMakeFiles/test_wavefunction.dir/clean:
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/test && $(CMAKE_COMMAND) -P CMakeFiles/test_wavefunction.dir/cmake_clean.cmake
.PHONY : test/CMakeFiles/test_wavefunction.dir/clean

test/CMakeFiles/test_wavefunction.dir/depend:
	cd /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/chiu.i-huan/Desktop/new_scientific/mudirac /Users/chiu.i-huan/Desktop/new_scientific/mudirac/test /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/test /Users/chiu.i-huan/Desktop/new_scientific/mudirac/build/test/CMakeFiles/test_wavefunction.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : test/CMakeFiles/test_wavefunction.dir/depend

