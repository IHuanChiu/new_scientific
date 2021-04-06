CC = g++
PROG = text2root
CXXFLAGS = -g -O2 -Wall -O -std=c++11
CPPFLAGS += -I$(shell ${ROOTSYS}/bin/root-config --incdir)
LDLIBS   += $(shell ${ROOTSYS}/bin/root-config --glibs) -O -std=c++11

all: $(PROG)

print : 
	$(PROG)
clean:
	rm -f *.o $(PROG)
