from keras.models import Model
from keras.models import Sequential
from keras.models import load_model
from keras import regularizers
from keras.layers import Input,Dense, Dropout, Activation
from keras.optimizers import SGD
#from keras.losses import logcosh
from keras.layers.normalization import BatchNormalization
def createModel(dim):
	model = Sequential()
	inputs = Input(shape=(dim,))
#model.add(Dropout(0.2))
#model.add(BatchNormalization())



	#b1 =  BatchNormalization()(inputs)
	#l1 =  Dense(100, kernel_initializer='RandomUniform',kernel_regularizer = regularizers.l2(1.00)  ,activation='relu')(inputs)#
	l1 =  Dense(150, kernel_initializer='RandomUniform',kernel_regularizer = regularizers.l2(0.001)   ,activation='tanh')(inputs)#
	d1 = Dropout(0.1)(l1)
	b1 =  BatchNormalization()(d1)
	
#model.add(Dense(100, kernel_initializer='RandomUniform', activation='relu'))
#model.add(Dropout(0.2))
#model.add(BatchNormalization())

	l2 = Dense(150, kernel_initializer='RandomUniform', kernel_regularizer = regularizers.l2(0.001)  ,activation='relu' )(b1)
	d2 = Dropout(0.1)(l2)
	b2 =  BatchNormalization()(d2)

	l3 = Dense(150, kernel_initializer='RandomUniform',kernel_regularizer = regularizers.l2(0.001)  , activation='relu' )(b2)
	d3 = Dropout(0.1)(l3)
	#b1 =  BatchNormalization()(d3)
	b3 =  BatchNormalization()(d3)

	l4 = Dense(150, kernel_initializer='RandomUniform',kernel_regularizer = regularizers.l2(0.001)  , activation='relu' )(b3)
	d4 = Dropout(0.1)(l4)
	b4 =  BatchNormalization()(d4)

#
#	b5=  BatchNormalization()(d4)
	l5 = Dense(100, kernel_initializer='RandomUniform',kernel_regularizer = regularizers.l2(0.001)  ,activation='relu' )(b4)
	d5 = Dropout(0.1)(l5)
	b5 =  BatchNormalization()(d5)







	out =  Dense(1, kernel_initializer='RandomUniform', activation='sigmoid')(l1)

	model  = Model(inputs = inputs, outputs = out)


	from keras.optimizers import Adam
	adam = Adam(lr=0.003)
	model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['acc'])
#	model.compile(loss='binary_crossentropy',  metrics=['mse'])

	return model 


