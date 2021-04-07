CC = g++
#PROG = binary2root binary2root2 eventbuild
PROG = text2root csv2root
CXXFLAGS = -g -O2 -Wall -O -std=c++11
CPPFLAGS += -I$(shell ${ROOTSYS}/bin/root-config --incdir)
LDLIBS   += $(shell ${ROOTSYS}/bin/root-config --glibs) -O -std=c++11
# LDLIBS += -L/usr/local/lib/ -lmylib


all: $(PROG)

print : 
	$(PROG)
clean:
	rm -f *.o $(PROG)


#CC=clang++
#CFLAGS=-c -g -Wall -L$(ROOTSYS)/lib -lMinuit
#CFLAGS2=$(shell root-config --libs) 
##LDFLAGS='root-config --glibs'
#SOURCES = text2root.C
#OBJECTS = text2root.o 
#TARGET  = text2root
#
#CXXFLAGS = -g -O2 -Wall -O -std=c++11 
#CPPFLAGS += -I$(shell ${ROOTSYS}/bin/root-config --incdir)
#LDLIBS   += $(shell ${ROOTSYS}/bin/root-config --glibs) -O -std=c++11 -lMinuit 
#
## =========================================================
#all :
#	$(TARGET)
#$(TARGET): 
#	$(SOURCES)
#
#.PHONY : help
#help :
#	@echo "Usage: make [options] [target] ..."
#	@echo "Targets:"
#	@grep -Eh '^[a-zA-Z_-]+ : .*?## .*$$' $(MAKEFILE_LIST) | sort | awk -F'[:##]' '{printf "  \033[0m%-25s\033[0m %s\n", $$1, $$4}'
#
#.PHONY : clean
#clean: ## Delete the targets and the objects.
#	-rm -f $(TARGET) $(TARGET2) *.o


# ========================= Meno ================================
#-o : specifies the output 
#-Wall: print all warning
#-g : gdb debugger
#-c : Compile into object .o file 

#$@: the target filename.
#$*: the target filename without the file extension.
#$<: the first prerequisite filename.
#$^: the filenames of all the prerequisites, separated by spaces, discard duplicates.
#$+: similar to $^, but includes duplicates.
#$?: the names of all prerequisites that are newer than the target, separated by spaces.
