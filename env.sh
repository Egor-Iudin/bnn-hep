#!/bin/bash
source /cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/gcc/7.0.0/etc/profile.d/init.sh
source /cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.14.09/bin/thisroot.sh
source /cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/tbb/2019_U8/etc/profile.d/init.sh


export PATH=`pwd`/bin:$PATH

export BOOST_LIBRARY_PATH=/cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/boost/1.67.0/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${BOOST_LIBRARY_PATH}lib/