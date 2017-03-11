import re

# Split with symbols `"`, space, `.`, `;`, `,`, `?`, `!`
split_symbols = ['\"',
			' ',
			'.',
			',',
			';',
			'?',
			'!']

def tokenize(sentence):
	words = [sentence]
	for symbol in split_symbols:
		words = split_with_delimiter(words, symbol)
	# Filter all the spaces among the tokens
	words = [ word for word in words if word!=' ']
	#words = [ word for word in words if word!=' 'and word!='.' and word!=';' and word!=',' and word!='?' and word!='!']
	return words

# Split ['Mr.Langdon','is','here.'] with `.` => ['Mr', '.', 'Langdon', 'is', 'here', '.']
def split_with_delimiter(words, delimiter):
	result = []
	for word in words:
		result += fill_with_delimiter(word.split(delimiter),delimiter)
	return filter(None, result)

# Fill [1,2,3] with d => [1,d,2,d,3]
def fill_with_delimiter(l, d):
	result = []
	for a in l:
		result += [a,d]
	return result[:-1]

if __name__ == "__main__":
	print tokenize('Mr. Langdon is here.')
	print tokenize('She turned to him, "This is great." she said.')