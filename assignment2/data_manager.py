import cPickle as pickle
import random

import numpy as np

class DataManager:

	def get_token_labels(self, filename='token_labels.pickle'):
		with open(filename,'rb') as f:
			return pickle.load(f)
	
	def get_tokens(self, filename='text8'):
		with open(filename,'r') as f:
			return f.readlines()[0].split()

	
	def get_word_to_label(self, filename='word2label.pickle'):
		with open(filename,'rb') as f:
			return pickle.load(f)

	def get_label2unigramf(self, filename='label2unigramf.pickle'):
		with open(filename, 'rb') as f:
			return pickle.load(f)

	def weighted_random_label(self):
		cumulative_f = [0]
		# For labels from 0 to 9999
		for label in range(len(self.label2unigramf.keys())):
			cumulative_f += [self.label2unigramf[label]+cumulative_f[-1]]

		x = random.randint(0,cumulative_f[-1])
		for i in range(len(cumulative_f)):
			if cumulative_f[i] > x:
				break

		return (i-1)

	def get_batch(self, minibatch_size,k):
		# If words left in the epoch are less than minibatch size, skip them and proceed to next epoch after shuffling
		if self.cur_batch_pointer+minibatch_size > len(self.token_labels):
			np.random.shuffle(self.token_indexes)
			self.cur_epoch += 1
			print
			print "Epoch: ",self.cur_epoch
			print
			self.cur_batch_pointer = 0
		# Pick a minibatch_size number of tokens from the corpus
		batch_token_indexes = self.token_indexes[self.cur_batch_pointer:self.cur_batch_pointer+minibatch_size]
		# Get labels of the tokens picked
		batch_token_labels = [self.token_labels[i] for i in batch_token_indexes]
		# Get labels of 2k surrounding tokens for each token picked
		contexts = [ self.token_labels[i-k:i]+self.token_labels[i+1:i+k+1] for i in batch_token_indexes]
		# Progess the pointer
		self.cur_batch_pointer += minibatch_size
		return contexts,batch_token_labels

	def __init__(self):

		self.label2unigramf = self.get_label2unigramf()

		"""
		tokens = self.get_tokens()
		word_to_label = self.get_word_to_label()

		token_labels = []
		for token in tokens:
			try:
				token_labels += [word_to_label[token]]
			except KeyError:
				token_labels += [len(word_to_label.values())]

		pickle.dump(token_labels,open('token_labels.pickle','wb'),pickle.HIGHEST_PROTOCOL)
		exit()
		"""


		# List of labels corresponding to each word in the corpus
		self.token_labels = self.get_token_labels()

		self.token_indexes = np.arange(len(self.token_labels))
		np.random.shuffle(self.token_indexes)
		# This is the pointer representing the point at which the next minibatch will be picked up
		self.cur_batch_pointer = 0

		self.cur_epoch = 1


		

if __name__ == '__main__':
	dataManager = DataManager()