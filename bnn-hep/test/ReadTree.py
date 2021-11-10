from rootpy.io import root_open
import numpy
import numpy.random
import root_numpy
import ROOT
import math as mt
import add_config
def readTree(fileName):
	rfile=ROOT.TFile(sampleName)
	tree=rfile.Get('Vars')
	array=root_numpy.tree2array(tree)
	print array	
	array_to_pred = array[cfg.inputVarNames]
	df = pd.DataFrame(array_to_pred)
	input_data = df.as_matrix()


#var1.shape
#a = np.array(var1,var2,var3,var4)

#//print var2
	i=1;
#weights_train = np.array([1.1]);
#labels_train = np.array([1.1]);
#data_train = np.array([1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]);
	labels = np.empty((0,1));
	weights = np.empty((0,1));
	data = np.empty((0, 42))
	
	for event in t: 
		data =	 np.append(data,	[event.var1,event.var2,event.var3,event.var4,event.var5,event.var6,event.var7,event.var8,event.var9,event.var10,event.var11,event.var12,event.var13,event.var14,event.var15,event.var16,event.var17,event.var18,event.var19,event.var20,event.var21,event.var22,event.var23,event.var24,event.var25,event.var26,event.var27,event.var28,event.var29,event.var30,event.var31,event.var32,event.var33,event.var34,event.var35,event.var36,event.var37,event.var38,event.var39,event.var40,event.var41,event.var42])
		labels = np.append(labels,[event.target])
#		labels_train.shape = (i,1)	
		weights = np.append(weights,[event.weight]);	
		i = i+1
	data.shape= (i-1,42)
	labels.shape = (i-1,1)	
		
	f.Close()
	return data,labels,weights
