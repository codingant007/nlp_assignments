import re

def sentence_segment(text):
	print "Raw Text:"
	print text
	print
	# Consider `!`, `?` and `.` as sentence boundaries and split
	sentences = split_by_boundary(text)
	print "Split by boundary:"
	print sentences
	print
	# Move boundary if `"` exists after `.`
	sentences = move_boundary(sentences)
	print "Move boundary:"
	print sentences
	print
	# Disqualify `.` if abbrevation
	sentences = merge_at_abbrevation(sentences)
	print "Merge at abbrevations:"
	print sentences
	print
	# Disqualify `!` and `?` if followed by lowercase
	sentences = merge_at_annotation(sentences)
	print "Disqualify annotations:"
	print sentences
	print
	# Filter the empty sentences
	sentences = filter(None, sentences)
	sentences = filter(lambda x: re.match(r' *',x) , sentences)
	print "Final filter for empty sentences"
	print sentences
	print
	return sentences

"""
	Split Heuristics
		- Consider the following as sentence boundaries
			- `!`
			- `?`
			- `.`

"""

def split_with_delimiter(text, delimiter):
	split = text.split(delimiter)
	return [ a+delimiter for a in split[:-1]] + [split[-1]] 

def split_by_boundary(text):
	# Split by `.`
	split_by_period = split_with_delimiter(text, '.')
	# Split by `!`
	split_by_exclamation = []
	for sentence in split_by_period:
		split_by_exclamation += split_with_delimiter(sentence, '!')
	# Split by '?'
	split_by_question = []
	for sentence in split_by_exclamation:
		split_by_question += split_with_delimiter(sentence, '?')
	return split_by_question

"""
	Handling Double quotes
		- Move the boundary if `"` exist
			- She turned to him, "This is great." she said.
			=> ["She turned to him, \"This is great.\" she said."]

"""
def move_boundary(sentences):
	result = [sentences[0]]
	for i in range(len(sentences)-1):
		# If there is a double quote in the sentence and next sentence begins with double quote
		if re.match(r'^.*\".*$',sentences[i]) and re.match(r'^ *\".*$',sentences[i+1]):
			# Double quote in next sentence is follwed by lowercase letter
			if re.match(r'^ *\" *[a-z].*$',sentences[i+1]):
				#Append to the last sentence
				result[-1] += sentences[i+1]
			# Double quote in the next sentence ends the sentence
			else:
				#Move double quote to the previous sentence
				result[-1] += "\""
				result += [re.sub(r'^ *\"(.*)$', r'\1', sentences[i+1])]
		else:
			result += [sentences[i+1]]
	return result

"""
	Abbrevation Heuristics
		- One letter uppercase
			- ['U.S.', 'A. Nikhil']
		- Two letter Upper
			- ['Mt. Everest', 'Mr. Langdon', 'Pitt Briggs & Co.', 'St. Louise Church', 'Frank Jr. is a funny man.']
		- One or Two letter words followed by non-capital alphabet
			- ['Jane and co. came to the party', 'turn to p. 35']
"""

known_abbrevations = ['co','Mrs']

def is_abbrevation(word):
	# One letter uppercase
	if re.match(r'^[A-Z]$', word):
		return True
	# Two letter first one uppercase
	if re.match(r'^[A-Z][A-Za-z]$', word):
		return True
	if word in known_abbrevations:
		return True
	# Not an abbrevation
	return False


def ends_with_abbrevation(sentence):
	m = re.match(r'^(.* )*(.*)\.', sentence)
	if m:
		if is_abbrevation(m.group(2)):
			return True
	return False

def merge_at_abbrevation(sentences):
	result = [sentences[0]]
	# From second sentence 
	for i in range(len(sentences)-1):
		# Append next sentence to ith if ith it ends with abbrevation
		if ends_with_abbrevation(sentences[i]):
			result[-1] += sentences[i+1]
		# Add next sentence if the current sentence doesn't end with abbrevation
		else:
			result += [sentences[i+1]]
	# Extra Heuristic when period is followed by lowecase letter
	result = merge_if_followed_by_lowecase(result)
	return result
# Extra heuristic for abbrevation when period is followed by lowecase
def merge_if_followed_by_lowecase(sentences):
	result = [sentences[0]]
	for i in range(len(sentences)-1):
		if re.match(r'.*\.$',sentences[i]) and re.match(r'^ *[a-z1-9]',sentences[i+1]):
			result[-1] += sentences[i+1]
		else:
			result += [sentences[i+1]]
	return result
"""
	Annotation Heuristics
		- Disqualify `.` if 
			- Preceeded by a valid abbrevation

		- Disqualify `!` or `?` if
			- Followed by lowercase.

"""
def merge_at_annotation(sentences):
	result = [sentences[0]]
	for i in range(len(sentences)-1):
		# Check if ith ends with annotation and i+1th begins with lower case
		# If yes append to next sentence
		if re.match(r'.*[\!\?]$',sentences[i]) and re.match(r'^ *[a-z1-9].*', sentences[i+1]):
			result[-1] += sentences[i+1]
		else:
		# Add next sentence else
			result += [sentences[i+1]]
	return result

if __name__ == "__main__":
	sentence_segment("St. Michael's Church is on 5th st. near the light.")
	sentence_segment("She turned to him, \"This is great.\" she said.")

