import theano
import theano.tensor as T 
import numpy as np

import paramDataManager
from data_manager import DataManager

import sys
sys.setrecursionlimit(50000)


negsample_count = 10
# Context window = 2*k+1 
k = 2
V = 10001
N = 50
minibatch_size = 1000
learning_rate = 0.01

def _make_shared(data, borrow=True):
	shared_data = theano.shared(np.asarray(data,
	 dtype=theano.config.floatX),
	borrow=borrow)
	return shared_data

class ContextLayer:

	def __init__(self, x, C, 
					minibatch_size):

		self.C = C
		# Array of vectors representing context h of each training sample in minibatch
		self.output = T.mean(C[x] , axis=1)

class WordLayer:

	def __init__(self, h, W, out_labels, neg, 
					minibatch_size):

		self.u_out = T.dot(W[y],h)
		#self.u_out = T.stack([ T.dot(W[out_labels[minibatch_index]], h[minibatch_index]) for minibatch_index in range(minibatch_size)])
		#neg_rows = [ W[neg[minibatch_index]]  for minibatch_index in range(minibatch_size)]
		self.u_neg = T.stack([ T.dot(neg_rows[minibatch_index], h[minibatch_index]) for minibatch_index in range(minibatch_size)])


class ObjectiveFunction:

	def __init__(self, u_out, u_neg, 
					minibatch_size):

		y_out = T.nnet.sigmoid(u_out)
		y_neg = T.nnet.sigmoid(-u_neg)

		E_out = -T.log(y_out)
		E_neg = -T.log(y_neg)

		self.output = T.sum(E_out) + T.sum(E_neg)

"""
C,D = paramDataManager.getParams(None, (V,N), (N,V))
"""

C = _make_shared(np.random.uniform(low=-0.1,high=0.1,size=(V,N)))
W = _make_shared(np.random.uniform(low=-0.1,high=0.1,size=(V,N)))

params = (C,W)

x = T.imatrix('x')
y = T.ivector('y')
neg = T.imatrix('neg')

contextLayer =  ContextLayer(x, C, minibatch_size)
h = contextLayer.output

wordLayer = WordLayer(h, W, y, neg, minibatch_size)

objectiveFunction = ObjectiveFunction(wordLayer.u_out, wordLayer.u_neg, minibatch_size)
loss = objectiveFunction.output

grads = T.grad(loss, params)
updates = [(param_i, param_i - learning_rate * grad_i) for param_i,grad_i in zip(params,grads)]

train_model = theano.function([x, y, neg], loss, updates=updates)


dataManager = DataManager()

minibatch_number = 0
epoch = 0

print "Enter"
while(True):
	if minibatch_number%1000 == 0:
		pickle.dump({'c': C.get_value(),
					 'w': W.get_value(),
					 'c_shape': C.get_shape(),
					 'w_shape': W.get_shape()
					}, open('params.pickle', 'wb'), pickle.HIGHEST_PROTOCOL)
	minibatch_number+= 1

	context_labels,output_labels = dataManager.get_batch(minibatch_size, k)
	negsample_labels = [ [ dataManager.weighted_random_label() for i in range(negsample_count)] for minibatch_index in range(minibatch_size)]


	cost = train_model(context_labels, output_labels, negsample_labels)
	print
	print "Minibatch: ",minibatch_number," Training loss: ",cost

