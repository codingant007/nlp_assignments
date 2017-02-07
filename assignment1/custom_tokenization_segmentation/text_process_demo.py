from sentence_segmentor import sentence_segment
from sentence_segmentor import *
from tokenizer import *

sentences = sentence_segment("I am Mrs. Alamanda. I enjoy typing endlessly! Oh! really? I do.")

print "Tokenized sentences:"
for sentence in sentences:
	print tokenize(sentence)