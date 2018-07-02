# CS Practice: Markov models and hash tables
# Edwin Gavis  
# Thanks to Anne Rogers

import sys
import math
import Hash_Table

HASH_CELLS = 57

class Markov:

    def __init__(self,k,s):
        '''
        Construct a new k-order Markov model using the statistics of string "s"
        '''
        self.k = k
        self.uniques = len(set(s))
        self.counts = Hash_Table.Hash_Table(HASH_CELLS, 0)
        self.fill_counts(s)

    def fill_counts(self,s):
        '''
        Add in the counts for each each k ("key") and k-1 ("stem") letter 
        combination in "s"
        '''
        for i in range(len(s)):
            key, stem = self.get_key_stem(s,i)
            current_count = self.counts.lookup(key)
            self.counts.update(key, current_count + 1)
            stem_count = self.counts.lookup(stem)
            self.counts.update(stem, stem_count + 1)

    def get_key_stem(self,s,i):
        '''
        Return the three and two letter keys corresponding to an index "i" 
        in string "s" 
        '''
        rv = str()
        for k_th in reversed(range(self.k + 1)):
            rv += s[i - k_th]
        return rv, rv[:-1]

    def log_probability(self,s):
        '''
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        '''
        rv = 0
        for i in range(len(s)):
            rv += self.get_log_prob(s, i)
        return rv

    def get_log_prob(self,s,i):
        '''
        Calculate the log probability of the character in string "s" at index "i"
        '''
        key, stem = self.get_key_stem(s,i)
        key_count = self.counts.lookup(key)
        stem_count = self.counts.lookup(stem)
        return math.log((1 + key_count) / (stem_count + self.uniques))


def identify_speaker(speech1, speech2, speech3, order):
    '''
    Given sample text from two speakers, and text from an unidentified speaker,
    return a tuple with the *normalized* log probabilities of each of the speakers
    uttering that text under a "order" order character-based Markov model,
    and a conclusion of which speaker uttered the unidentified text
    based on the two probabilities.
    '''
    modelA = Markov(order, speech1)
    modelB = Markov(order, speech2)
    log_probA = modelA.log_probability(speech3) / len(speech3)
    log_probB = modelB.log_probability(speech3) / len(speech3)
    if log_probA > log_probB:
        conclusion = "A"
    else:
        conclusion = "B"
    return (log_probA, log_probB, conclusion)


def print_results(res_tuple):
    '''
    Given a tuple from identify_speaker, print formatted results to the screen
    '''
    (likelihood1, likelihood2, conclusion) = res_tuple
    
    print("Speaker A: " + str(likelihood1))
    print("Speaker B: " + str(likelihood2))

    print("")

    print("Conclusion: Speaker " + conclusion + " is most likely")


if __name__=="__main__":
    #following by Anne Rogers
    num_args = len(sys.argv)

    if num_args != 5:
        print("usage: python3 " + sys.argv[0] + " <file name for speaker A> " +
              "<flie name for speaker B>\n  <file name of text to identify> " +
              "<order>")
        sys.exit(0)
    
    with open(sys.argv[1], "rU") as file1:
        speech1 = file1.read()

    with open(sys.argv[2], "rU") as file2:
        speech2 = file2.read()

    with open(sys.argv[3], "rU") as file3:
        speech3 = file3.read()

    res_tuple = identify_speaker(speech1, speech2, speech3, int(sys.argv[4]))

    print_results(res_tuple)


