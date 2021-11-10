#python trainModel.py --taskName bnn_sm --epochs 500 --batchSize 20000
# python trainModel.py --taskName BNN_tWb_8 --internalEpoch 20 --externalEepoch 10

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


def train(noweights,config,args,features_train, labels_train,weights_train, features_test, labels_test,weights_test):
	print 	args.model_arch
	dnn_model,dnn = ut.dynamic_importer(args.model_arch, "dnn")
	model = dnn.createModel(len(config.inputVarNames),args.layers)
	
	if args.batch_size ==0:
		args.batch_size = len(labels_train)
	print args.batch_size

	history = History()
	filepath=args.model_name+"best.h5"
	checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=2, save_best_only=True, mode='min')
	reduce_lr = ReduceLROnPlateau(monitor='val_mean_squared_error', factor=0.90,
                              patience=40, verbose=1)
	l_rate = 0.10	
	history_loss = []
	history_metric = []
	history_val_loss = []
	history_val_metric = []

	if noweights==True:
		print "Noweights"



		for ind in range(1,3):
			history = model.fit(features_train,labels_train,epochs=args.internal_epoch, batch_size=args.batch_size,shuffle=False, callbacks=[checkpoint,EarlyStopping(monitor='val_loss', patience =args.epochs/2),reduce_lr,],validation_data = (features_test,labels_test))
			model = ut.loadmodelH5(args.model_name+"best.h5")
			adam = Adam(lr=l_rate/((ind+1)*0.5))
			
			print "!!!!!!!!"
			print l_rate
			model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['mean_squared_error'])
			score = model.evaluate(features_test, labels_test, batch_size=args.batch_size, sample_weight =weights_test )

			print "!!!!!!!!"
			print score
		
	else:
		
		#history = model.fit(features_train,labels_train,epochs=args.epochs, batch_size=args.batch_size,shuffle=False, callbacks=[checkpoint,EarlyStopping(monitor='val_loss', patience =args.epochs/2),reduce_lr,],validation_data = (features_test,labels_test,weights_test), 		sample_weight = weights_train ,)
		for ind in range(1,args.internal_epoch):
			history  = model.fit(features_train,labels_train,epochs=args.internal_epoch, batch_size=args.batch_size,shuffle=False, callbacks=[checkpoint,EarlyStopping(monitor='val_loss', patience =args.epochs/2),reduce_lr,],validation_data = (features_test,labels_test,weights_test), 		sample_weight = weights_train ,)
			if ind!=(args.internal_epoch-1):
				model = ut.loadmodelH5(args.model_name+"best.h5")
			l_rate = l_rate*0.95				
			adam = Adam(lr=l_rate)
			for metric in history.history['loss']:
				history_loss.append(metric)
			for metric in history.history['val_loss']:
				history_val_loss.append(metric)
			for metric in history.history['mean_squared_error']:
				history_metric.append(metric)
			for metric in history.history['val_mean_squared_error']:
				history_val_metric.append(metric)
			#	history_metric.append(history.history['mean_squared_error'][metric_number])
			#	history_val_loss.append(history.history['val_loss'][metric_number])
			#	history_val_metric.append(history.history['val_mean_squared_error'][metric_number])
			print history_loss
		
			print "!!!!!!!!"
			print l_rate
#			model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['mean_squared_error'])
			score = model.evaluate(features_test, labels_test, batch_size=args.batch_size, sample_weight =weights_test )

			print "!!!!!!!!"
	
			print score


#		history = model.fit(features_train, labels_train,epochs=args.epochs, batch_size=args.batch_size, shuffle=False,callbacks=[checkpoint,EarlyStopping(monitor='val_loss', patience =args.epochs/2),reduce_lr,],validation_data = (features_test,labels_test,weights_test), 		sample_weight = weights_train )
			
#	score = model.evaluate(features_test, labels_test, batch_size=args.batch_size, sample_weight =weights_test )
	
	
	
	print "!!!!!!!!"

	print score

	print "!!!!!!!!"

	print model.metrics_names

	model.save(args.model_name+'.h5')
	plt.figure(1)
	plt.subplot(211)
        plt.plot(history_metric)
        plt.plot(history_val_metric)
        #plt.plot(history.history['mean_squared_error'])
	#plt.plot(history.history['val_mean_squared_error'])
	plt.title('model mse')
	plt.ylabel('mse')
	plt.xlabel('epoch')
	plt.legend(['train','test'], loc='upper left')
	#plt.savefig(task_name+'_Acc.png')
#	lt.show()

	#plt.figure(1)
	plt.subplot(212)
	plt.plot(history_loss)
        plt.plot(history_val_loss)
	#plt.plot(history.history['loss'])
	#plt.plot(history.history['val_loss'])
	plt.title('model loss')
	plt.ylabel('loss')
	plt.xlabel('epoch')
	plt.legend(['train', 'test'], loc='upper left')
	plt.savefig(args.model_name+'_loss.png')
#	plt.show()


	return model

if __name__ == "__main__":

	#task_name = "bnn_sm"
	#batch_size = 0
	#epochs = 1000
	#varNumber = 0
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

#	features_train, labels_train,weights_train, features_test, labels_test,weights_test,train_split_labels,test_split_labels,softmaxLabes_train,softmaxLabes_test = rd.ReadData(config)

	features_train, labels_train,weights_train, features_test, labels_test,weights_test = rd.ReadDataShort(config)
	predictList = []
	predictListbest = []
	#args.model_name = "ttbar_complite3L"+str(number)
	args.model_arch = "model_arch"
	args.batch_size = len(labels_train)
	#args.epochs= 100	
	model = train(False,config,args,features_train, labels_train,weights_train, features_test, labels_test,weights_test)
	args.model_name = args.model_name+"best"
	model = ut.loadmodelH5(args.model_name+".h5")
	pr.ShowPredictF(features_train, labels_train,weights_train, features_test, labels_test,weights_test,model,args)




# EnsembleTrain !!!!!!
#	predictList = []
#	predictListbest = []
#	for number in range(1,2):	
#		args.model_name = "ttbar_complite3L"+str(number)
#		args.model_arch = "model_arch"
#		args.batch_size = len(labels_train)
#		args.epochs= 100	
#		print features_train	
#		#args.model_name = "softmax"
#		model = train(3,False,config,args,features_train, labels_train,weights_train, features_test, labels_test,weights_test)
#		#args.model_name = "softmax"
#		#pr.ShowPredictF(features_train, labels_train,weights_train, features_test, labels_test,weights_test,model,args)
#		pr.ShowPredictBNN(features_train, labels_train,weights_train, features_test, labels_test,weights_test,model,args)
#		predictList.append( pr.ShowPredictF(features_train, labels_train,weights_train, features_test, labels_test,weights_test,model,args))

#		args.model_name = args.model_name+"best"
#		model = ut.loadmodelH5(args.model_name+".h5")
		#pr.ShowPredict(features_train, labels_train,weights_train, features_test, labels_test,weights_test,model,args)
#		predictListbest.append( pr.ShowPredictF(features_train, labels_train,weights_train, features_test, labels_test,weights_test,model,args))
#		pr.ShowPredictBNN(features_train, labels_train,weights_train, features_test, labels_test,weights_test,model,args)
#	print predictList
#	pr.ShowPredictEnsemble(features_train, labels_train,weights_train, features_test, labels_test,weights_test,model,args,predictListbest,2)
#	args.model_name = "ttbar_complite3L1"
	#model = ut.loadmodelH5(args.model_name+".h5")
#	pr.ShowPredictEnsemble(features_train, labels_train,weights_train, features_test, labels_test,weights_test,model,args,predictList,2)


	

