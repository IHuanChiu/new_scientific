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
include test/CMakeFiles/test_potential.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include test/CMakeFiles/test_potential.dir/compiler_depend.make

# Include the progress variables for this target.
include test/CMakeFiles/test_potential.dir/progress.make

# Include the compile flags for this target's objects.
include test/CMakeFiles/test_potential.dir/flags.make

test/CMakeFiles/test_potential.dir/test_potential.cpp.o: test/CMakeFiles/test_potential.dir/flags.make
test/CMakeFiles/test_potential.dir/test_potential.cpp.o: /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/test/test_potential.cpp
test/CMakeFiles/test_potential.dir/test_potential.cpp.o: test/CMakeFiles/test_potential.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object test/CMakeFiles/test_potential.dir/test_potential.cpp.o"
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/test && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT test/CMakeFiles/test_potential.dir/test_potential.cpp.o -MF CMakeFiles/test_potential.dir/test_potential.cpp.o.d -o CMakeFiles/test_potential.dir/test_potential.cpp.o -c /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/test/test_potential.cpp

test/CMakeFiles/test_potential.dir/test_potential.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/test_potential.dir/test_potential.cpp.i"
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/test && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/test/test_potential.cpp > CMakeFiles/test_potential.dir/test_potential.cpp.i

test/CMakeFiles/test_potential.dir/test_potential.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/test_potential.dir/test_potential.cpp.s"
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/test && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/test/test_potential.cpp -o CMakeFiles/test_potential.dir/test_potential.cpp.s

# Object files for target test_potential
test_potential_OBJECTS = \
"CMakeFiles/test_potential.dir/test_potential.cpp.o"

# External object files for target test_potential
test_potential_EXTERNAL_OBJECTS =

test/test_potential: test/CMakeFiles/test_potential.dir/test_potential.cpp.o
test/test_potential: test/CMakeFiles/test_potential.dir/build.make
test/test_potential: test/libtest_main.a
test/test_potential: lib/libdebugtasks.a
test/test_potential: lib/libconfig.a
test/test_potential: lib/liboutput.a
test/test_potential: lib/libatom.a
test/test_potential: lib/libboundary.a
test/test_potential: lib/libstate.a
test/test_potential: lib/libpotential.a
test/test_potential: lib/libeconfigs.a
test/test_potential: lib/libhydrogenic.a
test/test_potential: lib/libtransforms.a
test/test_potential: lib/libwavefunction.a
test/test_potential: lib/libintegrate.a
test/test_potential: lib/libelements.a
test/test_potential: lib/libinput.a
test/test_potential: lib/libutils.a
test/test_potential: test/CMakeFiles/test_potential.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable test_potential"
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/test_potential.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
test/CMakeFiles/test_potential.dir/build: test/test_potential
.PHONY : test/CMakeFiles/test_potential.dir/build

test/CMakeFiles/test_potential.dir/clean:
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/test && $(CMAKE_COMMAND) -P CMakeFiles/test_potential.dir/cmake_clean.cmake
.PHONY : test/CMakeFiles/test_potential.dir/clean

test/CMakeFiles/test_potential.dir/depend:
	cd /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac /Users/chiu.i-huan/Desktop/new_scientific/muDirac/mudirac/test /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/test /Users/chiu.i-huan/Desktop/new_scientific/muDirac/build/test/CMakeFiles/test_potential.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : test/CMakeFiles/test_potential.dir/depend

