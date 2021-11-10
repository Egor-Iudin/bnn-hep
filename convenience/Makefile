# Define the flags to control make
CC = g++
INCLUDE = -Iinclude -I../bnn-hep/include/ -I$(shell root-config --incdir) -I/cvmfs/sft.cern.ch/lcg/external/Boost/1.53.0_python2.7/x86_64-slc6-gcc48-opt/iclude/boost-1_53/
OPFLAGS = 
CFLAGS = -Wall -Wextra -std=c++11 $(INCLUDE) $(OPFLAGS)
LDFLAGS = $(shell root-config --libs) -L/cvmfs/sft.cern.ch/lcg/external/Boost/1.53.0_python2.7/x86_64-slc6-gcc48-opt/lib/ -lboost_filesystem-gcc48-mt-1_53 -lboost_system

vpath %.cpp src ../bnn-hep/src

# Define the phony targets
.PHONY: clean

# The default rule
all: eventIndexToID eventIDToIndex

eventIndexToID: eventIndexToID.o EventID.o TrainEventList.o
	$(CC) $(LDFLAGS) $+ -o $@
	@ cd ../bin; ln -sf ../convenience/$@; cd -

eventIDToIndex: eventIDToIndex.o EventID.o TrainEventList.o
	$(CC) $(LDFLAGS) $+ -o $@
	@ cd ../bin; ln -sf ../convenience/$@; cd -

%.o: %.cpp
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	@ rm -f *.o
	@ rm -f ../bin/eventIndexToID ../bin/eventIDToIndex
