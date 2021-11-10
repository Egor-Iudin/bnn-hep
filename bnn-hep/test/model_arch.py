from keras.models import Model
from keras.models import Sequential
from keras.models import load_model
from keras import regularizers
from keras.layers import Input,Dense, Dropout, Activation
from keras.optimizers import SGD
#from keras.losses import logcosh
from keras.layers.normalization import BatchNormalization

def returnLayaer(x,d1,d2,d3,d4,d5,d6,d7,d8):
	#print x    
	return {
        1: d1,
        2: d2,
        3: d3,
        4: d4,
        5: d5,
        6: d6,
        7: d7,
        8: d8,
        
    }[x] 

def createModel(dim,layers):
	model = Sequential()
	inputs = Input(shape=(dim,))
#model.add(Dropout(0.2))
#model.add(BatchNormalization())



	#b1 =  BatchNormalization()(inputs)
	#l1 =  Dense(100, kernel_initializer='RandomUniform',kernel_regularizer = regularizers.l2(1.00)  ,activation='relu')(inputs)#
#	l1 =  Dense(50, kernel_initializer='glorot_uniform',kernel_regularizer = regularizers.l2(0.001)   ,activation='sigmoid')(inputs)#
#	l1 =  Dense(50, kernel_initializer='glorot_uniform'   ,activation='sigmoid')(inputs)#
#	l1 =  Dense(120, kernel_initializer='RandomUniform',kernel_regularizer = regularizers.l1(0.0001)    ,activation='sigmoid')(inputs)#
	l1 =  Dense(100, kernel_initializer='uniform',kernel_regularizer = regularizers.l2(0.001)     ,activation='relu')(inputs)#

	d1 = Dropout(0.1)(l1)
	#b1 =  BatchNormalization()(d1)

	l2 =  Dense(100, kernel_initializer='uniform',kernel_regularizer = regularizers.l2(0.001)    ,activation='relu')(d1)#
	d2 = Dropout(0.2)(l2)
	#b2 =  BatchNormalization()(d2)	

	l3 =  Dense(100, kernel_initializer='uniform' ,kernel_regularizer = regularizers.l2(0.001)   ,activation='relu')(d2)#
	d3 = Dropout(0.2)(l3)
	#b3 =  BatchNormalization()(d3)	

	l4 =  Dense(100, kernel_initializer='uniform'  ,kernel_regularizer = regularizers.l2(0.001)  ,activation='relu')(d3)#
	d4 = Dropout(0.2)(l4)
	b4 =  BatchNormalization()(d4)

	l5 =  Dense(100, kernel_initializer='uniform'  ,kernel_regularizer = regularizers.l2(0.001)  ,activation='relu')(d4)#
	d5 = Dropout(0.1)(l5)
	b5 =  BatchNormalization()(d5)


	l6 =  Dense(50, kernel_initializer='he_uniform',kernel_regularizer = regularizers.l2(0.00001)   ,activation='relu')(b5)#
	d6 = Dropout(0.2)(l6)
	b6 =  BatchNormalization()(d6)


	l7 =  Dense(50, kernel_initializer='he_uniform',kernel_regularizer = regularizers.l2(0.001)   ,activation='relu')(b6)
	d7 = Dropout(0.2)(l7)
	b7 =  BatchNormalization()(d7)

	l8 =  Dense(50, kernel_initializer='he_uniform',kernel_regularizer = regularizers.l2(0.001)   ,activation='relu')(b7)#
	d8 = Dropout(0.1)(l8)
	b8 =  BatchNormalization()(d8)	

#	l9 =  Dense(100, kernel_initializer='RandomUniform',kernel_regularizer = regularizers.l2(0.001)   ,activation='relu')(d8)
#	d9 = Dropout(0.1)(l9)
#

#	l10 =  Dense(100, kernel_initializer='RandomUniform',kernel_regularizer = regularizers.l2(0.001)   ,activation='relu')(d9)#
#	d10 = Dropout(0.1)(l10)








	out =  Dense(1, kernel_initializer='glorot_uniform', activation='sigmoid')(returnLayaer(layers,d1,d2,d3,d4,d5,d6,d7,d8))
#	out =  Dense(1, kernel_initializer='RandomUniform', activation='sigmoid')(d2)


	model  = Model(inputs = inputs, outputs = out)


	from keras.optimizers import Adam,SGD
	sgd = SGD(lr=0.5)
	adam = Adam(lr=0.03)
	model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['mean_squared_error'])
#	model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['mean_squared_error'])
#	model.compile(loss='binary_crossentropy',  metrics=['mse'])

	return model 


