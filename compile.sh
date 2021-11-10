rm libCROOT.a ;

gcc -O -pthread -m64 -I/cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.24.06/x86_64-centos7-gcc48-opt/root/include -c CTGraph.cxx -o CTGraph.o;
ar -cvq libCROOT.a  CTGraph.o;
gcc -L/cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.24.06/x86_64-centos7-gcc48-opt/root/lib -lCore -lCint -lRIO -lNet -lHist -lGraf -lGraf3d -lGpad -lTree -lRint -lPostscript -lMatrix -lPhysics -lMathCore -lThread -pthread -lm -ldl -rdynamic printError.cxx libCROOT.a  libCROOT.a -lm -o printError;




