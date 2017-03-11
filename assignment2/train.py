import theano
import theano.tensor as T 
import numpy as np

import paramDataManager


negsample_count = 10
# Context window = 2*k+1 
k = 2
V = 10000
N = 50
minibatch_size = 512

def _make_shared(data, borrow=True):
	shared_data = theano.shared(np.asarray(data,
	 dtype=theano.config.floatX),
	borrow=borrow)
	return shared_data


class ContextLayer:

	def __init__(self, x, minibatch_size, k, N):

		#assert (x.shape == (minibatch_size, 2*k, N)), "Context layer input shape error"
			
		# Array of vectors representing context h of each training sample in minibatch
		self.output = T.stack([ T.mean(x[minibatch_index], axis=0) for minibatch_index in range(minibatch_size)])

		#assert (self.output.shape == (minibatch_size,N) )

class WordLayer:

	def __init__(self, h, z, neg,
					minibatch_size, N, negsample_count):
		"""
		assert (h.shape == (minibatch_size, N)), "Word layer input shape error"
		assert (neg.shape == (minibatch_size, negsample_count)), "Word layer negative sample shape error"
		assert(z.shape == (minibatch_size)), "Word layer output label shape error"
		"""
		self.u_out = T.stack([T.dot(h[minibatch_index], z[minibatch_index]) for minibatch_index in range(minibatch_size)])
		#self.u_neg = T.stack([ T.stack([ T.dot(h[minibatch_index], sample) for sample in neg[minibatch_index]]) for minibatch_index in range(minibatch_size)])
		
		self.u_neg = T.stack([T.dot(h[minibatch_index], neg[minibatch_index]) for minibatch_index in range(minibatch_size)])

		"""
		assert (self.u_neg.shape == (minibatch_size, negsample_count))
		assert (self.u_out.shape == (minibatch))
		"""

class ObjectiveFunction:

	def __init__(self, u_out, u_neg, minibatch_size, negsample_count):
		"""
		assert (self.u_neg.shape == (minibatch_size, negsample_count))
		assert (self.u_out.shape == (minibatch))
		"""

		y_out = T.nnet.sigmoid(u_out)
		y_neg = T.nnet.sigmoid(-u_neg)

		E_out = -T.log(y_out)
		E_neg = -T.log(y_neg)

		self.output = T.sum(E_out) + T.sum(E_neg)

x = T.tensor3('x')
z = T.matrix('z')
neg = T.tensor3('neg')

"""
params = paramDataManager.getParams(None, (V,N), (V,N))

C = params[0]
W = params[1]
"""

C = _make_shared(np.random.uniform(low=-0.1,high=0.1,size=(V,N)))
W = _make_shared(np.random.uniform(low=-0.1,high=0.1,size=(V,N)))

params = (C,W)

contextLayer = ContextLayer(x, minibatch_size, k, N)
h = contextLayer.output

wordLayer = WordLayer(h, z, neg, minibatch_size, N, negsample_count)

objectiveFunction = ObjectiveFunction(wordLayer.u_out, wordLayer.u_neg, minibatch_size, negsample_count)
loss = objectiveFunction.output

grads = T.grad(loss, params)

updates = [(param_i, param_i - learning_rate * grad_i) for param_i,grad_i in zip(params,grads)]

train_model = theano.function([x,z,neg], loss, updates=updates)


while(True):
	contexts,token_labels = data_manager.getBatch(minibatch_size, k)
	negsamples = [ [ data_manager.weighted_random_label() for i in range(negsample_count)] for minibatch_index in range(minibatch_size)]

	# Each minibatch has a matrix (2k,N)
	context_vecs = np.asarray([ [ C[i] for i in contexts[minibatch_index]] for minibatch_index in range(minibatch_size)])

	# Each minibatch has a vector (N) representing the output word
	output_word_vec = np.asarray([ W[token_labels[minibatch_index]] for minibatch_index in range(minibatch_size)])
	# Each minibatch has a matrix (neg_count,N) ie one vector per negative sample
	negsample_vecs = np.asarray([ [ W[negsample_label] for negsample_label in negsamples[minibatch_index]] for minibatch_index in range(minibatch_size)])

	cost = train_model(context_vecs, output_word_vec, negsample_vecs)