#!/usr/bin/env python
"""reducer.py"""
from operator import itemgetter
import sys

word_counts = {}

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from mapper.py
    word, count = line.split('\t', 1)
    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue
    
    # Update the word count
    if word in word_counts:
        word_counts[word] += count
    else:
        word_counts[word] = count

# Sort the word_counts dictionary by value (count) in descending order
sorted_word_counts = sorted(word_counts.items(), key=itemgetter(1), reverse=True)

# Output the sorted results
for word, count in sorted_word_counts:
    print('%s\t%s' % (word,count))
