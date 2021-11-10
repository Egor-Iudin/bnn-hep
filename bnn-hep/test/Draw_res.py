import sys
import numpy as np
import matplotlib.pyplot as plt
import imp
import utils
from keras.optimizers import Adam,SGD
#import DNNmodel as dnn
import ReadData as rd
import utils as ut

import PredictResult as pr

from keras.callbacks import History 
from keras.callbacks import EarlyStopping 
from keras.callbacks import ModelCheckpoint
from keras.callbacks import ReduceLROnPlateau

task_name = "bnn_sm"
batch_size = 0
epochs = 1000
varNumber = 0
for ind in range(len(sys.argv)):
	if sys.argv[ind] == "--varNumber":
		varNumber = int(sys.argv[ind+1]) 
		print "varNumber",varNumber	

print str(sys.argv)   	
args = ut.dnn_args()
	#task_name,batch_size,epochs = ut.get_args(task_name,batch_size,epochs)
args.get_args(sys.argv)	
cfg,config  = ut.dynamic_importer(args.task_name+"C", "config")
#cfg,config  = ut.dynamic_importer(args.task_name+"C", "config")

features_train, labels_train,weights_train, features_test, labels_test,weights_test,train_split_labels,test_split_labels,softmaxLabes_train,softmaxLabes_test = rd.ReadData(config)
args.model_name = "ttbar_complite3L1"
model = ut.loadmodelH5(args.model_name+".h5")

pr.ShowPredictBNN(features_train, labels_train,weights_train, features_test, labels_test,weights_test,model,args,'top_ttbar_complite_3layer')


