from scipy.sparse import dok_matrix
from numpy.random import choice
import glob
import random


class CS370InANutshell:
    def __init__(self):
        self.makeChain()

    def makeChain(self):
        # clean files
        corpus = ""
        # open all .txt files in the listed directory
        file_names = glob.glob('./Utils/lectureTextFiles/*.txt')
        for file_name in file_names:
            with open(file_name, 'r') as f:
                corpus += f.read()
        corpus = corpus.replace('\n', ' ')
        corpus = corpus.replace('\t', ' ')
        corpus = corpus.replace('“', ' " ')
        corpus = corpus.replace('”', ' " ')
        # added to list as found in testing
        for removed in ['—', '°', '|', '-', '•', '', ':', '}', '{', '"', ''
                        ';', ')', '(', '=', '+', '%', '<', '>', '#', '–', 'U+F06C']:
            corpus = corpus.replace(removed, '')
        for spaced in ['.', ',', '!', '?']:
            corpus = corpus.replace(spaced, ' {0} '.format(spaced))
        corpus_words = corpus.split(' ')
        # onlu use words that are not blank or numbers
        corpus_words = [word for word in corpus_words if word != '' and not word.isdecimal()]

        # train
        self.distinct_words = list(set(corpus_words))
        word_idx_dict = {word: i for i, word in enumerate(self.distinct_words)}
        k = 2
        self.sets_of_k_words = [' '.join(corpus_words[i:i+k]) for i, _ in enumerate(corpus_words[:-k])]
        sets_count = len(list(set(self.sets_of_k_words)))
        self.next_after_k_words_matrix = dok_matrix((sets_count, len(self.distinct_words)))

        distinct_sets_of_k_words = list(set(self.sets_of_k_words))
        self.k_words_idx_dict = {word: i for i, word in enumerate(distinct_sets_of_k_words)}

        for i, word in enumerate(self.sets_of_k_words[:-k]):
            word_sequence_idx = self.k_words_idx_dict[word]
            next_word_idk = word_idx_dict[corpus_words[i+k]]
            self.next_after_k_words_matrix[word_sequence_idx, next_word_idk] += 1

    # select a the next word based on the preious and the likelihood that the word appears
    def sample_next_word_after_sequence(self, word_sequence, alpha=0):
        next_word_vector = self.next_after_k_words_matrix[self.k_words_idx_dict[word_sequence] + alpha]
        likelihoods = next_word_vector/next_word_vector.sum()
        return choice(self.distinct_words, p=likelihoods.toarray()[0])

    # make a chain of words that fit the given lengths
    def stochastic_chain(self, seed, max_length=50, min_length=20, seed_length=2):
        current_words = seed.split(' ')
        if len(current_words) != seed_length:
            raise ValueError(f'wrong number of words, expected {seed_length}')
        sentence = seed

        length = 0
        next_word = 'Start'  # arbitrary value since it is overwritten
        while (length < max_length and (next_word != '.' or length < min_length)):
            sentence += ' '
            next_word = self.sample_next_word_after_sequence(' '.join(current_words))
            sentence += next_word
            current_words = current_words[1:]+[next_word]
            length += 1
        return sentence

    # finds a starting point that is not a period or comma so that the output looks better
    # uses a max_attempts value because the random nature of selection could take forever
    def getSeed(self, max_attempts=20):
        attempts = 0
        seed = random.choice(self.sets_of_k_words)
        while (attempts < max_attempts and
               (seed[0] == ',' or seed[0] == '.')):
            seed = random.choice(self.sets_of_k_words)
            attempts += 1
        return seed

    def getContent(self, cl):
        # cl is 1-100 concenetration level
        message_variability = 30
        max = cl
        min = max - message_variability
        if min <= 0:
            min = 1
        seed = self.getSeed(30)
        body = self.stochastic_chain(seed, seed_length=2, max_length=max, min_length=min)
        return body.capitalize()


if __name__ == "__main__":
    content = CS370InANutshell()
    print(content.getContent())
