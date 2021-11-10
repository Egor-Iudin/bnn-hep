from keras.models import Model
from keras.models import Sequential
from keras.models import load_model
from keras import regularizers
from keras.layers import Input,Dense, Dropout, Activation
from keras.optimizers import SGD
#from keras.losses import logcosh
from keras.layers.normalization import BatchNormalization
import imp
import sys
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


def loadmodelH5(prefics1):
	model = load_model(prefics1)
	return model
class dnn_args:

	task_name = "bnn_sm"
	batch_size = 0
	epochs = 100
	model_arch = "model"
	model_name = ""
	layers = 3 
	internal_epoch = 4 
	external_epoch = 4
	branch_name = "DNN"
        tree_name = "Vars"

	def __init(self):
		task_name = "bnn_sm"
		batch_size = 0
		epochs = 100
		model_arch = "model_arch"
		model_name = ""
		layers = 3 
		internal_epoch = 4 
		external_epoch = 4		
		branch_name = "DNN"
		tree_name = "Vars"
	def get_args(self,args):
		for ind in range(len(args)):
			if args[ind] == "--taskName":
				self.task_name = args[ind+1] 
				print "task_name",self.task_name		
			if args[ind] == "--batchSize":
				self.batch_size = int(args[ind+1]) 		
  			if args[ind] == "--epochs":
				print self.epochs
				self.epochs = int(args[ind+1]) 		
			if args[ind] == "--modelArch":
				self.model_arch = args[ind+1] 		
			if args[ind] == "--modelName":
				self.model_name = args[ind+1] 		

			if args[ind] == "--layers":
				self.layers = int(args[ind+1]) 		

			if args[ind] == "--internalEpoch":
				self.internal_epoch = int(args[ind+1]) 		

			if args[ind] == "--externalEepoch":
				self.external_epoch = int(args[ind+1]) 	

			if args[ind] == "--branchName":
				self.branch_name = args[ind+1]		

			if args[ind] == "--treeName":
				self.tree_name = args[ind+1]		


		if self.model_name == "":
				self.model_name = self.task_name
			


		#return task_name,batch_size,epochs,model_arch,
