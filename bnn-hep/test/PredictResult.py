import numpy as np
import matplotlib.pyplot as plt
import ROOT as rt
import sys
from array import array
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from keras import metrics

from math import sqrt
#from rootpy.plotting import Hist,HistStack
import utils as ut
import ReadData as rd


def signifence(labels, predict, weights ):
	nbins =100
	binsSign = np.zeros(nbins,dtype=np.double)
	binsBack = np.zeros(nbins,dtype=np.double)
	binsSignWeight = np.zeros(nbins,dtype=np.double)
	binsBackWeight = np.zeros(nbins,dtype=np.double)
	sign =0.0
	for eventNumber in range(0,len(labels)-1):
		for binnumber in range(0,nbins-1):
			#print binnumber/nbins
			low = binnumber/(nbins*1.0)
			hight = (binnumber+1)/(nbins*1.0)
			#print low,hight
			if (predict[eventNumber]>low) and (predict[eventNumber]<=hight):
				if (labels[eventNumber] == 0 ):
					#print predict[eventNumber]
					binsBack[binnumber]=binsBack[binnumber]+1
					binsBackWeight[binnumber]= binsBackWeight[binnumber]+weights[eventNumber]

				else:
					#print predict[eventNumber]
					binsSign[binnumber]=binsSign[binnumber]+1
					binsSignWeight[binnumber]= binsSignWeight[binnumber]+weights[eventNumber]
	for binnumber in range(0,nbins-1):
		if (binsSign[binnumber]!=0 and  binsSignWeight[binnumber]!=0 ):
			#sign =sign+ binsSign[binnumber]*binsSignWeight[binnumber]/sqrt(binsSign[binnumber]*binsSignWeight[binnumber]+binsBackWeight[binnumber]*binsBack[binnumber])*(1/(nbins*1.0))
			sign =sign+ binsSign[binnumber]/sqrt(binsSign[binnumber]+binsBack[binnumber])*(1/(nbins*1.0))


	return sign


#dim = int(sys.argv[3])



def ShowPredict(config,model,args):
	features_train, labels_train,weights_train, features_test, labels_test,weights_test,train_split_labels,test_split_labels,softmaxLabes_train,softmaxLabes_test = rd.ReadData(config)
	#features_train, labels_train, features_test, labels_test,weights_train,weights_test = load_datasets(prefics)
	labels_train_backgrount = labels_train[np.where(labels_train < 1.0)]
	labels_train_signal = labels_train[np.where(labels_train >= 1.0)]
	labels_test_backgrount = labels_test[np.where(labels_test < 1.0)]
	labels_test_signal = labels_test[np.where(labels_test >= 1.0)]
	train_len = len(labels_train_signal)
	test_len =  len(labels_test_signal)
	predict_test = model.predict(features_test)
	predict_train = model.predict(features_train)
	predict_signal_test = predict_test[:test_len]
	predict_background_test = predict_test[test_len:]
	weight_signal_test = weights_test[:test_len]
	weight_background_test = weights_test[test_len:]
	#predict_train = model.predict(features_train)
	predict_signal_train = predict_train[:train_len]
	predict_background_train = predict_train[train_len:]
	weight_signal_train = weights_train[:train_len]
	weight_background_train = weights_train[train_len:]
	roc_test = roc_auc_score(labels_test,predict_test, sample_weight = weights_test)
	roc_train = roc_auc_score(labels_train,predict_train,sample_weight = weights_train)


	title = 'roc_auc_test='+"{0:.3f}".format(round(roc_test,3))+' roc_auc_train='+"{0:.3f}".format(round(roc_train,3))
	plt.clf()
	plt.hist(predict_signal_test, 20 ,histtype='step',color='g',normed =1,label = 'test_signal',weights = weight_signal_test)
	plt.hist(predict_background_test, 20 ,histtype='step',color='y',normed =1,label = 'test_background',weights = weight_background_test)
	plt.hist(predict_signal_train, 20 ,histtype='step',color='r',normed =1,linestyle='--',label = 'train_signal',weights = weight_signal_train)
	plt.hist(predict_background_train, 20 ,histtype='step',color='b',normed =1,linestyle='--',label = 'train_background',weights = weight_background_train)



	plt.legend(loc="upper center")
	plt.xlabel(title )
	plt.savefig(args.model_name+'_Discr.pdf')
	plt.savefig(args.model_name+'_Discr.png')

	plt.clf()
	fpr_bnn, tpr_bnn, _ = roc_curve(labels_train, predict_train,sample_weight = weights_train)

	fpr_dnn, tpr_dnn, _ = roc_curve(labels_test, predict_test,sample_weight = weights_test)


	plt.figure(1)
	plt.plot([0, 1], [0, 1], 'k--')
#plt.plot(fpr_rt_lm, tpr_rt_lm, label='RT + LR')
	plt.plot(fpr_bnn, tpr_bnn, 'r--',label='train')
	plt.plot(fpr_dnn, tpr_dnn,'b-', label='test')


#//plt.plot(fpr_rf_lm, tpr_rf_lm, label='RF + LR')
#plt.plot(fpr_grd, tpr_grd, label='GBT')
#plt.plot(fpr_grd_lm, tpr_grd_lm, label='GBT + LR')
	plt.xlabel('False positive rate')
	plt.ylabel('True positive rate')
	plt.title('ROC curve')
	plt.legend(loc='best')
	plt.savefig(args.model_name+'_ROC.pdf')
	plt.savefig(args.model_name+'_ROC.png')




def ShowPredictF(features_train, labels_train,weights_train, features_test, labels_test,weights_test,model,args):


	labels_train_backgrount = labels_train[np.where(labels_train < 1.0)]
	labels_train_signal = labels_train[np.where(labels_train >= 1.0)]
	labels_test_backgrount = labels_test[np.where(labels_test < 1.0)]
	labels_test_signal = labels_test[np.where(labels_test >= 1.0)]

	train_len = len(labels_train_signal)
	test_len =  len(labels_test_signal)
	predict_test = model.predict(features_test)
	predict_train = model.predict(features_train)



	predict_signal_test = predict_test[:test_len]
	predict_background_test = predict_test[test_len:]
	weight_signal_test = weights_test[:test_len]
	weight_background_test = weights_test[test_len:]
	#predict_train = model.predict(features_train)
	predict_signal_train = predict_train[:train_len]
	predict_background_train = predict_train[train_len:]
	weight_signal_train = weights_train[:train_len]
	weight_background_train = weights_train[train_len:]


#roc_bnn = roc_auc_score(labels_test,bnn_predict,sample_weight = bnn_weights)
	roc_test = roc_auc_score(labels_test,predict_test, sample_weight = weights_test)
	roc_train = roc_auc_score(labels_train,predict_train,sample_weight = weights_train)
#title = 'roc_auc='+str(roc)+' roc_auc_bnn='+str(roc_bnn)

	title = 'roc_auc_test='+"{0:.3f}".format(round(roc_test,3))+' roc_auc_train='+"{0:.3f}".format(round(roc_train,3))
	plt.clf()
	plt.hist(predict_signal_test, 20 ,histtype='step',color='g',normed =1,label = 'test_signal',weights = weight_signal_test)
	plt.hist(predict_background_test, 20 ,histtype='step',color='y',normed =1,label = 'test_background',weights = weight_background_test)
	plt.hist(predict_signal_train, 20 ,histtype='step',color='r',normed =1,linestyle='--',label = 'train_signal',weights = weight_signal_train)
	plt.hist(predict_background_train, 20 ,histtype='step',color='b',normed =1,linestyle='--',label = 'train_background',weights = weight_background_train)
	plt.legend(loc="upper center")
	plt.xlabel(title )
	plt.savefig(args.model_name+'_Discr.pdf')
	plt.savefig(args.model_name+'_Discr.png')
	plt.clf()


	fpr_bnn, tpr_bnn, _ = roc_curve(labels_train, predict_train,sample_weight = weights_train)
	fpr_dnn, tpr_dnn, _ = roc_curve(labels_test, predict_test,sample_weight = weights_test)


	plt.figure(1)
	plt.plot([0, 1], [0, 1], 'k--')
	plt.plot(fpr_bnn, tpr_bnn, 'r--',label='train')
	plt.plot(fpr_dnn, tpr_dnn,'b-', label='test')
	plt.xlabel('False positive rate')
	plt.ylabel('True positive rate')
	plt.title('ROC curve')
	plt.legend(loc='best')
	plt.savefig(args.model_name+'_ROC.pdf')
	plt.savefig(args.model_name+'_ROC.png')

	return predict_test


def ShowPredictBNN(features_train, labels_train,weights_train, features_test, labels_test,weights_test,model,args,fig_name):


	# = rd.ReadData(config)
	#features_train, labels_train, features_test, labels_test,weights_train,weights_test = load_datasets(prefics)


	labels_train_backgrount = labels_train[np.where(labels_train < 1.0)]
	labels_train_signal = labels_train[np.where(labels_train >= 1.0)]
	labels_test_backgrount = labels_test[np.where(labels_test < 1.0)]
	labels_test_signal = labels_test[np.where(labels_test >= 1.0)]

	train_len = len(labels_train_signal)
	test_len =  len(labels_test_signal)
	predict_test = model.predict(features_test)
	predict_train = model.predict(features_train)



	predict_signal_test = predict_test[:test_len]
	predict_background_test = predict_test[test_len:]
	weight_signal_test = weights_test[:test_len]
	weight_background_test = weights_test[test_len:]
	#predict_train = model.predict(features_train)
	predict_signal_train = predict_train[:train_len]
	predict_background_train = predict_train[train_len:]
	weight_signal_train = weights_train[:train_len]
	weight_background_train = weights_train[train_len:]
	bnn_labels = np.genfromtxt('BNN_target.txt')
	bnn_predict  = np.genfromtxt('BNN_pred.txt')
	bnn_weights  = np.genfromtxt('BNN_weight.txt')
	print "dnn_weights"

	print weights_test
	print "bnn_weights"
	print bnn_weights
	#bnn_weights = weights_test
#bnn_labels = np.genfromtxt('bnn_tug_target.txt')
#print len(bnn_labels)
#bnn_predict  = np.genfromtxt('bnn_sm_conv_pred.txt')
#bnn_weights  = np.genfromtxt('bnn_sm_conv_weight.txt')
#bnn_labels = labels_test


	bnn_labels_backgrount = labels_test[np.where(labels_test < 1.0)]
	bnn_labels_signal = labels_test[np.where(labels_test >= 1.0)]
	bnn_len =  len(bnn_labels_signal)

	bnn_signal = bnn_predict[:bnn_len]
	bnn_background = bnn_predict[bnn_len:]
	bnn_weight_signal = bnn_weights[:bnn_len]
	bnn_weight_background = bnn_weights[bnn_len:]


#roc_bnn = roc_auc_score(labels_test,bnn_predict,sample_weight = bnn_weights)
	roc_test = roc_auc_score(labels_test,predict_test, sample_weight = weights_test)
	roc_train = roc_auc_score(bnn_labels,bnn_predict,sample_weight = bnn_weights)
#title = 'roc_auc='+str(roc)+' roc_auc_bnn='+str(roc_bnn)

#	title = 'roc_auc_DNN='+"{0:.3f}".format(round(roc_test,3))+' roc_auc_BNN='+"{0:.3f}        ".format(round(roc_train,3))
	#title = ''
	plt.clf()

	plt.hist(predict_signal_test, 21 ,histtype='step',color='g',normed =True,label = 'DNN_signal',weights = weight_signal_test)
	plt.hist(predict_background_test, 21 ,histtype='step',color='y',normed =True,label = 'DNN_background',weights = weight_background_test)

#	plt.hist(bnn_signal, 20 ,histtype='step',color='r',linestyle=':',normed =1,label = 'BNN_signal',weights = bnn_weight_signal)

#	plt.hist(bnn_background, 20 ,histtype='step',color='b',linestyle=':',normed =1,label = 'BNN_background',weights = bnn_weight_background)
	plt.hist(bnn_signal, 21 ,histtype='step',color='r',normed =True,linestyle='--', linewidth=2,label = 'BNN_signal',weights = bnn_weight_signal)

	plt.hist(bnn_background, 21 ,histtype='step',color='b',normed =True,linestyle='--', linewidth=2,label = 'BNN_background',weights = bnn_weight_background)



	plt.legend(loc="upper center")
#	plt.set_ylim(0,4.7)
	#plt.grid(True)


	



	plt.xlabel("NNout" )
	plt.ylabel("1/N dN/dNNout" )
#	plt.ylabel("Nevents" )
	plt.savefig(fig_name+'_Discr.pdf')
	plt.savefig(fig_name+'_Discr.png')


#	plt.show()

	plt.clf()
	fpr_bnn, tpr_bnn, _ = roc_curve(labels_test, bnn_predict,sample_weight = bnn_weights)

	fpr_dnn, tpr_dnn, _ = roc_curve(labels_test, predict_test,sample_weight = weights_test)


	plt.figure(1)
	#plt.plot([0, 1], [0, 1], 'k--')
#plt.plot(fpr_rt_lm, tpr_rt_lm, label='RT + LR')
	plt.plot(fpr_bnn, tpr_bnn, 'r--',linewidth=2,label='BNN ROC curve'+' (auc='+"{0:.3f}".format(round(roc_train,3))+')')
	plt.plot(fpr_dnn, tpr_dnn,'b-', label='DNN ROC curve'+' (auc='+"{0:.3f}".format(round(roc_test,3))+')')
#title = '
	

#//plt.plot(fpr_rf_lm, tpr_rf_lm, label='RF + LR')
#plt.plot(fpr_grd, tpr_grd, label='GBT')
#plt.plot(fpr_grd_lm, tpr_grd_lm, label='GBT + LR')
	plt.xlabel('Specificity')
	plt.ylabel('Sensitivity')
	plt.title('ROC curve')
	plt.legend(loc='best')
	plt.savefig(fig_name+'_ROC.pdf')
	plt.savefig(fig_name+'_ROC.png')


	return predict_test



def ShowPredictEnsemble(features_train, labels_train,weights_train, features_test, labels_test,weights_test,model,args,predictList, eCount ):


	# = rd.ReadData(config)
	#features_train, labels_train, features_test, labels_test,weights_train,weights_test = load_datasets(prefics)


	labels_train_backgrount = labels_train[np.where(labels_train < 1.0)]
	labels_train_signal = labels_train[np.where(labels_train >= 1.0)]
	labels_test_backgrount = labels_test[np.where(labels_test < 1.0)]
	labels_test_signal = labels_test[np.where(labels_test >= 1.0)]

	train_len = len(labels_train_signal)
	test_len =  len(labels_test_signal)
	predict_train = model.predict(features_train)

	

	predictEn = predictList[0]
	for predNumber in range (1,eCount-1):
		print predNumber
		#predict =  predictList[startN:startN+len(labels_train)-1]
		#startN = startN+len(labels_train)
		predictEn = predictEn +predictList[predNumber]
	print predictEn
	print len(predictEn)
	predict_test = predictEn/(eCount	-1)
	print predict_test
	predict_signal_test = predict_test[:test_len]
	predict_background_test = predict_test[test_len:]
	weight_signal_test = weights_test[:test_len]
	weight_background_test = weights_test[test_len:]
	#predict_train = model.predict(features_train)
	predict_signal_train = predict_train[:train_len]
	predict_background_train = predict_train[train_len:]
	weight_signal_train = weights_train[:train_len]
	weight_background_train = weights_train[train_len:]
	bnn_labels = np.genfromtxt('BNN_target.txt')
	bnn_predict  = np.genfromtxt('BNN_pred.txt')
	bnn_weights  = np.genfromtxt('BNN_weight.txt')
#bnn_labels = np.genfromtxt('bnn_tug_target.txt')
#print len(bnn_labels)
#bnn_predict  = np.genfromtxt('bnn_sm_conv_pred.txt')
#bnn_weights  = np.genfromtxt('bnn_sm_conv_weight.txt')
#bnn_labels = labels_test


	bnn_labels_backgrount = labels_test[np.where(labels_test < 1.0)]
	bnn_labels_signal = labels_test[np.where(labels_test >= 1.0)]
	bnn_len =  len(bnn_labels_signal)

	bnn_signal = bnn_predict[:bnn_len]
	bnn_background = bnn_predict[bnn_len:]
	bnn_weight_signal = bnn_weights[:bnn_len]
	bnn_weight_background = bnn_weights[bnn_len:]


#roc_bnn = roc_auc_score(labels_test,bnn_predict,sample_weight = bnn_weights)
	roc_test = roc_auc_score(labels_test,predict_test, sample_weight = weights_test)
	roc_train = roc_auc_score(bnn_labels,bnn_predict,sample_weight = bnn_weights)
#title = 'roc_auc='+str(roc)+' roc_auc_bnn='+str(roc_bnn)

	title = 'roc_auc_DNN='+"{0:.3f}".format(round(roc_test,3))+' roc_auc_BNN='+"{0:.3f}".format(round(roc_train,3))
	plt.clf()
	plt.hist(predict_signal_test, 20 ,histtype='step',color='g',normed =1,label = 'DNN_signal',weights = weight_signal_test)

	plt.hist(predict_background_test, 20 ,histtype='step',color='y',normed =1,label = 'DNN_background',weights = weight_background_test)

	plt.hist(bnn_signal, 20 ,histtype='step',color='r',normed =1,label = 'BNN_signal',weights = bnn_weight_signal)

	plt.hist(bnn_background, 20 ,histtype='step',color='b',normed =1,label = 'BNN_background',weights = bnn_weight_background)

	#return predict_test


	

	plt.legend(loc="upper center")

	#plt.grid(True)






	plt.xlabel(title )
	plt.savefig(args.model_name+"Ensemble_BNN"+'_Discr.pdf')
#	plt.show()

	plt.clf()
	fpr_bnn, tpr_bnn, _ = roc_curve(labels_test, bnn_predict,sample_weight = bnn_weights)

	fpr_dnn, tpr_dnn, _ = roc_curve(labels_test,predict_test,sample_weight = weights_test)


	plt.figure(1)
	plt.plot([0, 1], [0, 1], 'k--')
#plt.plot(fpr_rt_lm, tpr_rt_lm, label='RT + LR')
	plt.plot(fpr_bnn, tpr_bnn, 'r--',label='BNN')
	plt.plot(fpr_dnn, tpr_dnn,'b-', label='DNN')


#//plt.plot(fpr_rf_lm, tpr_rf_lm, label='RF + LR')
#plt.plot(fpr_grd, tpr_grd, label='GBT')
#plt.plot(fpr_grd_lm, tpr_grd_lm, label='GBT + LR')
#	plt.xlabel('False positive rate')
#	plt.ylabel('True positive rate')
	plt.xlabel('Specificity')
	plt.ylabel('Sensitivity')
	plt.title('ROC curve')
	plt.legend(loc='best')
	plt.savefig(args.model_name+"Ensemble_BNN"+'_ROC.pdf')


def ShowPredictSoftMax(config,model,args):


	features_train, labels_train,weights_train, features_test, labels_test,weights_test,train_split_labels,test_split_labels,softmaxLabes_train,softmaxLabes_test = rd.ReadData(config)
	#features_train, labels_train, features_test, labels_test,weights_train,weights_test = load_datasets(prefics)

	#labels_train = labels_train[:,1]
	#labels_test = labels_test[:,1]
	labels_train_backgrount = labels_train[np.where(labels_train< 1.0)]
	labels_train_signal = labels_train[np.where(labels_train >= 1.0)]
	labels_test_backgrount = labels_test[np.where(labels_test < 1.0)]
	labels_test_signal = labels_test[np.where(labels_test >= 1.0)]
	print labels_test_signal
	train_len = len(labels_train_signal)
	test_len =  len(labels_test_signal)
	predict_test = model.predict(features_test)
	predict_train = model.predict(features_train)



	predict_signal_test = predict_test[:test_len,1]
	predict_background_test = predict_test[test_len:,1]
	weight_signal_test = weights_test[:test_len]
	weight_background_test = weights_test[test_len:]
	#predict_train = model.predict(features_train)
	predict_signal_train = predict_train[:train_len,1]
	predict_background_train = predict_train[train_len:,1]
	weight_signal_train = weights_train[:train_len]
	weight_background_train = weights_train[train_len:]




#roc_bnn = roc_auc_score(labels_test,bnn_predict,sample_weight = bnn_weights)
	roc_test = roc_auc_score(labels_test,predict_test[:,1], sample_weight = weights_test)
	roc_train = roc_auc_score(labels_train,predict_train[:,1],sample_weight = weights_train)
#title = 'roc_auc='+str(roc)+' roc_auc_bnn='+str(roc_bnn)

	title = 'roc_auc_test='+"{0:.3f}".format(round(roc_test,3))+' roc_auc_train='+"{0:.3f}".format(round(roc_train,3))
	plt.clf()
	plt.hist(predict_signal_test, 20 ,histtype='step',linestyle='-.',color='g',normed =1,label = 'test_signal',weights = weight_signal_test)

	plt.hist(predict_background_test, 20 ,histtype='step',linestyle='-.',color='y',normed =1,label = 'test_background',weights = weight_background_test)

	plt.hist(predict_signal_train, 20 ,histtype='step',color='r',normed =1,label = 'train_signal',weights = weight_signal_train)

	plt.hist(predict_background_train, 20 ,histtype='step',color='b',normed =1,label = 'train_background',weights = weight_background_train)


	


	plt.legend(loc="upper center")

	#plt.grid(True)






	plt.xlabel(title )
	plt.savefig(args.model_name+'_Discr.png')
#	plt.show()






if __name__ == "__main__":
	task_name = "bnn_sm"
	batch_size = 0
	epochs = 100

	#print str(sys.argv)   	
	args = ut.dnn_args()
	args.get_args(sys.argv)	
	#task_name,batch_size,epochs = ut.get_args(task_name,batch_size,epochs)
	cfg,config  = ut.dynamic_importer(args.task_name+"C", "config")
	model = ut.loadmodelH5(args.model_name+".h5")
	ShowPredict(config,model,args.task_name)
