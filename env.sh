#!/bin/bash
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.24.06/x86_64-centos7-gcc48-opt/bin/thisroot.sh
source  /cvmfs/sft.cern.ch/lcg/external/gcc/4.8.4/x86_64-slc6-gcc48-opt/setup.sh /cvmfs/sft.cern.ch/lcg/contrib

export PATH=`pwd`/bin:$PATH
export BOOST_LIBRARY_PATH=/cvmfs/sft.cern.ch/lcg/external/Boost/1.53.0_python2.7/x86_64-slc6-gcc48-opt/
export BOOST_VERSION="1-53"