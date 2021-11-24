#!/bin/bash
source /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/gcc/9.3.0/etc/profile.d/init.sh
source /cvmfs/cms.cern.ch/slc7_amd64_gcc900/lcg/root/6.22.08/bin/thisroot.sh
source /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/tbb/2020_U3/etc/profile.d/init.sh


export PATH=`pwd`/bin:$PATH

export BOOST_LIBRARY_PATH=/cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/boost/1.75.0/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${BOOST_LIBRARY_PATH}lib/