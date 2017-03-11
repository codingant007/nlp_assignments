from text_processor import *
from storage_manager import *
import operator

def get_cumulative_frequency(tuples):
	cf = [("dummy",0)]
	for token, frequency in tuples:
		cf += [(token, cf[-1][1] + frequency)]
	# Remove the dummy and return
	return cf[1:]

def get_number_before_threshold(cf, threshold):
	for i in range(len(cf)):
		if cf[i][1] > threshold:
			return i

# Get text from brown corpus
print "Getting raw text..."
text = get_raw_text()
# Get total, unigram, bigram and trigram frequencies in three dictionaries
print "Processing text..."
frequencies = process_text(text)
total_frequency,unigram_frequency,bigram_frequency,trigram_frequency = frequencies
print "Processing done."
# Dump the dictionaries to secondary storage
dump_frequencies(frequencies)
print "Total Frequency:"
print total_frequency
#print unigram_frequency
#print bigram_frequency
#print trigram_frequency

unigram_coverage_threshold = 90*total_frequency/100
bigram_coverage_threshold = 80*total_frequency/100
trigram_coverage_threshold = 70*total_frequency/100

# Frequency tuples in increasing order of the frequencies
unigram_frequency = list(reversed(sorted(unigram_frequency.items(), key=operator.itemgetter(1))))
bigram_frequency = list(reversed(sorted(bigram_frequency.items(), key=operator.itemgetter(1))))
trigram_frequency = list(reversed(sorted(trigram_frequency.items(), key=operator.itemgetter(1))))

# Get cumulative frequency mapping
unigram_cf = get_cumulative_frequency(unigram_frequency)
bigram_cf = get_cumulative_frequency(bigram_frequency)
trigram_cf = get_cumulative_frequency(trigram_frequency)


# Get number of tokens required to cross the threshold
unigram_count = get_number_before_threshold(unigram_cf, unigram_coverage_threshold)
bigram_count = get_number_before_threshold(bigram_cf, bigram_coverage_threshold)
trigram_count = get_number_before_threshold(trigram_cf, trigram_coverage_threshold)

print
print "Number of unigrams for 90% coverage:"
print unigram_count
print
print"Number of bigrams for 80% coverage:" 
print bigram_count
print
print"Number of bigrams for 70% coverage:" 
print trigram_count
print



