#  https://cms-ml.github.io/documentation/inference/tensorflow2.html
export SCRAM_ARCH="slc7_amd64_gcc900"
export CMSSW_VERSION="CMSSW_11_2_3"

source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsrel "$CMSSW_VERSION"
cd $CMSSW_VERSION
cmsenv

# source /cvmfs/cms.cern.ch/slc7_amd64_gcc900/lcg/root/6.22.06/bin/thisroot.sh
# source /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/gcc/9.3.0/etc/profile.d/init.sh
# source /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/python3/3.8.2/etc/profile.d/init.sh
# source /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/boost/1.75.0/etc/profile.d/init.sh
