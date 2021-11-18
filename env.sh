#!/bin/bash
source /cvmfs/cms.cern.ch/slc7_amd64_gcc900/lcg/root/6.22.08/bin/thisroot.sh
source /cvmfs/sft.cern.ch/lcg/external/gcc/4.8.4/x86_64-slc6-gcc48-opt/setup.sh /cvmfs/sft.cern.ch/lcg/contrib

export PATH=`pwd`/bin:$PATH

export BOOST_LIBRARY_PATH=/cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/boost/1.75.0/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"$BOOST_LIBRARY_PATH"lib/