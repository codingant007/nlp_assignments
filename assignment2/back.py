import theano
import theano.tensor as T 

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

def get_word_embedding(filename='')

class ContextLayer:

	# Returns the vector form of context rows averaged
	def get_h(self, x):
		#context_rows = T.stack([self.C[i] for i in x])
		context_rows,_ = theano.scan(lambda x: C[])
		return T.mean(context_rows, axis=0)

	def __init__(self, x, C, minibatch_size, k, V, N):
		self.x = x
		self.C = C

		assert (x.shape == (minibatch_size, 2*k)), "Context layer input shape error"
		assert (C.shape == (minibatch_size, V, N)), "Context layer parameter shape error"
		
		# Array of vectors
		self.output = T.stack([ self.get_h(x[minibatch_index]) for minibatch_index in range(minibatch_size)])

		assert (self.output.shape == (minibatch_size,N) )

class WordLayer:

	def get_u(self, h, j):
		W_T = self.W.T
		return T.dot(W_T[j], h)

	def __init__(self, h, W, out_label, negsample_indexes, 
					minibatch_size, N, V, negsample_count):
		self.h = h
		self.W = W

		assert(h.shape == (minibatch_size, N)), "Word layer input shape error"
		assert(W.shape == (minibatch_size, N, V)), "Word layer parameter shape error"
		assert(negsample_indexes.shape == (minibatch_size, negsample_count)), "Word layer negative sample shape error"
		assert(out_label.shape == (minibatch_size)), "Word layer output label shape error"

		self.u_out = T.stack(get_u(out_label))
		self.u_neg = T.stack([T.stack([get_u(j) for j in negsample_indexes[minibatch_index]]) for minibatch_index in range(minibatch_size)])

		self.u_neg.shape == (minibatch_size, negsample_count)


C,D = paramDataManager.getParams(None, (V,N), (N,V))

j_list = T.ivector('j_list')
#negsample_indexes = get_weighted_random_indexes((minibatch_size, negsample_count))
negsample_indexes = T.dmatrix('negsample_indexes')

x = [ [ L(i) for i in range(-k,k+1) if i != 0] for j in j_list]

contextLayer =  ContextLayer(x, C, minibatch_size, k, V, N)

h = contextLayer.output


train_model = theano.function([j_list, negsample_indexes], E, updates=updates)

x = T.dmatrix('x')
j_list = T.ivector('j_list')

contextLayer =  ContextLayer(x, C, minibatch_size, k, V, N)
h = contextLayer.output

wordLayer = WordLayer(h, W, minibatch_size, N, V)
wordLayer.output

train_model = theano.function(inputs=[x,j_list], outputs=E, updates=updates)



class ContextLayer:

	def __init__(self, x, minibatch_size, k, N):

		assert (x.shape == (minibatch_size, 2*k, N)), "Context layer input shape error"
			
		# Array of vectors representing context h of each training sample in minibatch
		self.output = T.stack([ T.mean(x[minibatch_index], axis=0) for minibatch_index in range(minibatch_size)])

		assert (self.output.shape == (minibatch_size,N) )

class WordLayer:

	def __init__(self, h, z, neg,
					minibatch_size, N, negsample_count):

		assert (h.shape == (minibatch_size, N)), "Word layer input shape error"
		assert (neg.shape == (minibatch_size, negsample_count)), "Word layer negative sample shape error"
		assert(z.shape == (minibatch_size)), "Word layer output label shape error"

		self.u_out = T.stack([T.dot(h[minibatch_index], z[minibatch_index]) for minibatch_index in range(minibatch_index)])
		self.u_neg = T.stack([ T.stack([ T.dot(h[minibatch_index], sample[minibatch_index]) for sample in neg[minibatch_index]]) for minibatch_index in range(minibatch_size)])

		assert (self.u_neg.shape == (minibatch_size, negsample_count))
		assert (self.u_out.shape == (minibatch))

Class ObjectiveFunction:

	def __init__(self, u_out, u_neg, minibatch_size, negsample_count):

		assert (self.u_neg.shape == (minibatch_size, negsample_count))
		assert (self.u_out.shape == (minibatch))

		y_out = T.nnet.sigmoid(u_out)
		y_neg = T.nnet.sigmoid(-u_neg)

		E_out = -T.log(y_out)
		E_neg = -T.log(y_neg)

		self.output = sum(y_out) + sum(y_neg)




C,W = paramDataManager.getParams(None, (V,N), (V,N))

params = [C, W]

x = T.tensor3('x')
z = T.matrix('z')
neg = T.tensor3('neg')

contextLayer = ContextLayer(x, minibatch_size, k, N)
h = contextLayer.output

wordLayer = WordLayer(h, z, neg, minibatch_size, N, negsample_count)

objectiveFunction = ObjectiveFunction(wordLayer.u_out, wordLayer.u_neg, minibatch_size, negsample_count)
loss = objectiveFunction.output

grads = T.grad(loss, params)

updates = [(param_i, param_i - learning_rate * grad_i) for param_i,grad_i in zip(params,grads)]

train_model = theano.function(inputs=[x,z,neg], loss, updates=updates)


while(True):
	contexts,words = data_manager.getBatch()
	negsamples = [ [ weighted_random_index() for i in range(negsample_count)] for minibatch_index in range(minibatch_size)]

	# Each minibatch has a matrix (2k,N)
	context_h = np.asarray([ [ C[i] for i in contexts[minibatch_index]] for minibatch_index in range(minibatch_size)])

	# Each minibatch has a vector (N) representing the output word
	output_word_vec = np.asarray([ W[words[minibatch_index]] for minibatch_index in range(minibatch_size)])
	# Each minibatch has a matrix (neg_count,N) ie one vector per negative sample
	negsample_vecs = np.asarray([ [ W[negsample_index] for negsample_index in negsamples[minibatch_index]] for minibatch_index in range(minibatch_size)])

	cost = train_model(context_h, output_word_vec, negsample_vecs)