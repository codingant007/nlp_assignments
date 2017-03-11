import theano

import cPickle as pickle
import numpy as np

def _make_shared(data, borrow=True):
	shared_data = theano.shared(np.asarray(data,
	 dtype=theano.config.floatX),
	borrow=borrow)
	return shared_data

def getParams(filename, C_shape, W_shape):
	C = []
	W = []
	if filename == None:
		C = np.random.uniform(low=-0.1,high=0.1,size=C_shape)
		W = np.random.uniform(low=-0.1,high=0.1,size=W_shape)
	else:
		with open(filename,'rb') as f:
			data = pickle.load(f)
			assert (data['c_shape'] == C_shape)
			assert (data['w_shape'] == W_shape)
			C = data['c']
			W = data['w']
	return (_make_shared(C),_make_shared(W))

		

def saveParams(filename, C, W):
	pickle.dump({'c': C.get_value(),
				 'w': W.get_value(),
				 'c_shape': C.get_shape(),
				 'w_shape': W.get_shape()
				}, open(filename, 'wb'), pickle.HIGHEST_PROTOCOL)