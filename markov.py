# CS Practice: Markov models and hash tables
# Edwin Gavis  
# Special thanks to Matthew Wachs

import sys
import math
import Hash_Table

HASH_CELLS = 57
ORDER = 2

def main():
    with open("speechA.txt", "rU") as f1:
        a_speech = f1.read()
    with open("speechB.txt", "rU") as f2:
        b_speech = f2.read()
    with open("speechX.txt", "rU") as f3:
        unknown = f3.read()
    modelA = Markov(ORDER, a_speech)
    modelB = Markov(ORDER, b_speech)
    log_probA = modelA.log_probability(unknown) / len(unknown)
    log_probB = modelB.log_probability(unknown) / len(unknown)
    print ("Probability Speaker A: " + str(log_probA))
    print ("Probability Speaker B: " + str(log_probB))


class Markov:

    def __init__(self,k,s):
        self.k = k
        self.uniques = len(set(s))
        self.counts = Hash_Table.Hash_Table(HASH_CELLS, 0)
        self.fill_counts(s)

    def fill_counts(self,s):
        for i in range(len(s)):
            key, stem = self.get_key_stem(s,i)
            current_count = self.counts.lookup(key)
            self.counts.update(key, current_count + 1)
            stem_count = self.counts.lookup(stem)
            self.counts.update(stem, stem_count + 1)

    def get_key_stem(self,s,i):
        rv = str()
        for k_th in reversed(range(self.k + 1)):
            rv += s[i - k_th]
        return rv, rv[:-1]

    def log_probability(self,s):
        rv = 0
        for i in range(len(s)):
            rv += self.get_log_prob(s, i)
        return rv

    def get_log_prob(self,s,i):
        key, stem = self.get_key_stem(s,i)
        key_count = self.counts.lookup(key)
        stem_count = self.counts.lookup(stem)
        return math.log((1 + key_count) / (stem_count + self.uniques))


if __name__=="__main__":
    main()
