#python ReadData.py  qcd_trainFile_170527_170056_pjy.root qcd_examFile_170527_171257_GUR.root QCD
import ROOT as rt
import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib.mlab as mlab
import ReadTree as rt
import importlib
import numpy.random
import root_numpy
import ROOT
import imp
import pandas as pd
#import bnn_smC.py
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

def splitLabel(labels):
	splitLables =  []
	for val in labels:
		splitLables.append(parsesample(val))
	return splitLables

def softMaxLabels(labels):
	softMaxLabel =  []
	for val in labels:
		softMaxLabel.append(softmaxSample(val))
	return softMaxLabel

def parsesample(x):
	#print x    
	return {
        0: [1,0,0,0,0,0,0,0,0],
        1: [1,0,0,0,0,0,0,0,0],
        2: [1,0,0,0,0,0,0,0,0],
        3: [0,1,0,0,0,0,0,0,0],
        4: [0,0,1,0,0,0,0,0,0],
        5: [0,0,0,1,0,0,0,0,0],
        6: [0,0,0,1,0,0,0,0,0],
        7: [0,0,0,0,1,0,0,0,0],
        8: [0,0,0,0,0,1,0,0,0],
        9: [0,0,0,0,0,0,1,0,0],
        10: [0,0,0,0,0,0,0,1,0],
        11: [0,0,0,0,0,0,0,0,1],
        12: [0,0,0,0,0,0,0,0,1]
        
    }[x] 
def softmaxSample(x):
	#print x    
	return {
        0: [1,0],
        1: [0,1]
        
    }[x] 

def ReadSample(sampleName,config):
	
	inputVars = []
	for index in range(len(config.inputVarNames)):
		varName = "var"+str(index+1)		
		inputVars.append(varName)	
	#print inputVars
	rfile=ROOT.TFile(sampleName)
	tree=rfile.Get('Vars')
	array=root_numpy.tree2array(tree)
	data_array = array[inputVars]
	data_df = pd.DataFrame(data_array)

	weights_array = array["weight"]
	weights_df = pd.DataFrame(weights_array)
	#print "Weights"	
	#print weights_df
	target_array = array["target"]
	target_df = pd.DataFrame(target_array)
	input_data = data_df.as_matrix()
	#weights_array = np.genfromtxt('BNN_weight.txt')
	input_weight = weights_array
	input_target = target_array

	sampleNumbers = array["sampleNumber"]
	#print sampleNumbers	
  	splitLabels =  np.array(splitLabel(sampleNumbers))
	softmaxLabes = np.array(softMaxLabels(target_array))
	print softmaxLabes	
	print splitLabels
	#print input_data,input_weight,input_target
	return input_data,input_target,input_weight,splitLabels,softmaxLabes

	#for var_index in range(len(cfg.inputVarNames)):
	#	input_data[:,var_index] = (input_data[:,var_index] -cfg.mean[var_index]) / cfg.sigma[var_index];
	#	print  cfg.inputVars[var_index]


#f1 = rt.TFile.Open("qcd_trainFile_170527_182646_XaN.root","read")
#f1 = rt.TFile.Open("qcd_examFile_170527_171257_GUR.root","read")
#t1 = f1.Get("Vars")
#var1.shape
#a = np.array(var1,var2,var3,var4)

#//print var2

def ReadData(config):
	#train_split_labels
	data_train,labels_train,weights_train,train_split_labels,softmaxLabes_train = ReadSample(config.trainFileName,config)
	data_test,labels_test,weights_test,test_split_labels,softmaxLabes_test = ReadSample(config.examFileName,config)
#	print data_train.shape,labels_train.shape,weights_train.shape,data_test.shape,labels_test.shape,weights_test.shape,train_split_labels.shape,test_split_labels.shape

	return data_train,labels_train,weights_train,data_test,labels_test,weights_test,train_split_labels,test_split_labels,softmaxLabes_train,softmaxLabes_test


def ReadDataShort(config):
	#train_split_labels
	data_train,labels_train,weights_train,train_split_labels,softmaxLabes_train = ReadSample(config.trainFileName,config)
	data_test,labels_test,weights_test,test_split_labels,softmaxLabes_test = ReadSample(config.examFileName,config)
#	print data_train.shape,labels_train.shape,weights_train.shape,data_test.shape,labels_test.shape,weights_test.shape,train_split_labels.shape,test_split_labels.shape

	return data_train,labels_train,weights_train,data_test,labels_test,weights_test



#labels_test = np.array([1.0]);
if __name__ == "__main__":


	task_Name = sys.argv[1]
	#config = task_Name+"C"

#	module,config  = dynamic_importer("/afs/cern.ch/work/p/pvolkov/public/QCD_bnn_and_dnn/addDNNExample/"+task_Name+"C.py", "	config")
	cfg,config  = dynamic_importer(task_Name+"C", "config")
	print str(sys.argv)   	


	features_train, labels_train, features_test, labels_test,weights_train,weights_test = ReadData(config)
	print features_train, labels_train, features_test, labels_test,weights_train,weights_test






#predict = model.predict(features_test,batch_size=100000)


#np.set_printoptions(threshold=np.nan)
#print predict.shape
#print predict

#n, bins, patches = plt.hist(predict, 100, normed=1, facecolor='green')



