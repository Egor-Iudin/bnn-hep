import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import add_config as cfg
#from sklearn.metrics import roc_auc_score
#from sklearn.metrics import roc_curve
from keras import metrics
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from math import sqrt
import pandas as pd
from rootpy.io import root_open
import numpy
import numpy.random
import root_numpy
import ROOT
import math as mt
from keras.models import model_from_yaml
import imp

import utils as ut

def dynamic_importer(name, class_name):
    """
    Dynamically imports modules / classes
    """
    try:
        fp, pathname, description = imp.find_module(name)
    except ImportError,e:
        print e
        print "unable to locate module: " + name
        return (None, None)
 
    try:
        example_package = imp.load_module(name, fp, pathname, description)
    except Exception, e:
        print e
 
    try:
        myclass = imp.load_module("%s.%s" % (name, class_name), fp, pathname, description)
        print myclass
    except Exception, e:
        print e
 
    return example_package, myclass


def addDNN(args, sampleName):

	cfg1,config  = dynamic_importer(args.task_name+"C", "config")
	rfile=ROOT.TFile(sampleName)
	tree=rfile.Get(args.tree_name)
	array=root_numpy.tree2array(tree,branches=cfg1.inputVarNames)
	print array	
	array_to_pred = array[cfg1.inputVarNames]
	df = pd.DataFrame(array_to_pred)
	input_data = df.as_matrix()
	#print([b.GetName() for b in tree.GetListOfBranches()])  # prints ['n_int', 'f_float', 'd_double']
	
	print input_data
	for var_index in range(len(cfg1.inputVarNames)):
		input_data[:,var_index] = (input_data[:,var_index] -cfg1.means[var_index]) / cfg1.sigmas[var_index];
		print  cfg1.inputVarNames[var_index]

	#model = loadmodelH5(prefics1)
	model = ut.loadmodelH5(args.model_name+".h5")
	predict = model.predict(input_data)
	#with root_open(sampleName, mode='a') as myfile:
	new_column = numpy.array(predict , dtype=[(args.branch_name, 'f8')])
	root_numpy.array2root(new_column, sampleName, args.tree_name)
	#	root_numpy.array2tree(new_column, tree=myfile.Vars)
	#	myfile.write()
#	plt.hist(predict, histtype='step', normed=False, bins=40, label='dnn_out', linewidth=2)
	#plt.show()
	print predict	

if __name__ == "__main__":
	
	args = ut.dnn_args()
        args.get_args(sys.argv)	
	dirs = [
#"/afs/cern.ch/work/p/pvolkov/public/Networks/13Tev/samples/tuples_merged/UnclMETDown/",
	"./samples/"
	]
#loadmodel(prefics1)

#path = str(sys.argv[2])

for path in dirs:
	sample_files = [f for f in os.listdir(path) if f.endswith('.root')]
	for root_file in sample_files:
		print root_file
		addDNN(args, path+ root_file)
