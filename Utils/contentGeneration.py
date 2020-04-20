from scipy.sparse import dok_matrix
from numpy.random import choice
import glob
import random

# clean file
corpus = ""
file_names = glob.glob('./lectureTextFiles/*.txt')
for file_name in file_names:
    with open(file_name, 'r') as f:
        corpus += f.read()
corpus = corpus.replace('\n', ' ')
corpus = corpus.replace('\t', ' ')
corpus = corpus.replace('“', ' " ')
corpus = corpus.replace('”', ' " ')
for removed in ['—', '°', '|', '-', '•', '', ':', '}', '{', ';', ')', '(', '=', '+', '%', '<', '>', '#']:
    corpus = corpus.replace(removed, '')
for spaced in ['.', ',', '!', '?']:
    corpus = corpus.replace(spaced, ' {0} '.format(spaced))
corpus_words = corpus.split(' ')
corpus_words = [word for word in corpus_words if word != '' and not word.isdecimal()]
print("Total of " + str(len(corpus_words)) + " words.")

# train
distinct_words = list(set(corpus_words))
word_idx_dict = {word: i for i, word in enumerate(distinct_words)}
print("Total of " + str(len(distinct_words)) + " unique words.")
k = 2
sets_of_k_words = [' '.join(corpus_words[i:i+k]) for i, _ in enumerate(corpus_words[:-k])]
sets_count = len(list(set(sets_of_k_words)))
next_after_k_words_matrix = dok_matrix((sets_count, len(distinct_words)))

distinct_sets_of_k_words = list(set(sets_of_k_words))
k_words_idx_dict = {word: i for i, word in enumerate(distinct_sets_of_k_words)}

for i, word in enumerate(sets_of_k_words[:-k]):
    word_sequence_idx = k_words_idx_dict[word]
    next_word_idk = word_idx_dict[corpus_words[i+k]]
    next_after_k_words_matrix[word_sequence_idx, next_word_idk] += 1


def sample_next_word_after_sequence(word_sequence, alpha=0):
    next_word_vector = next_after_k_words_matrix[k_words_idx_dict[word_sequence] + alpha]
    likelihoods = next_word_vector/next_word_vector.sum()
    return choice(distinct_words, p=likelihoods.toarray()[0])


def stochastic_chain(seed, max_length=50, min_length=20, seed_length=2):
    current_words = seed.split(' ')
    if len(current_words) != seed_length:
        raise ValueError(f'wrong number of words, expected {seed_length}')
    sentence = seed

    length = 0
    next_word = 'Start'
    while (length < max_length and (next_word != '.' or length < min_length)):
        sentence += ' '
        next_word = sample_next_word_after_sequence(' '.join(current_words))
        sentence += next_word
        current_words = current_words[1:]+[next_word]
        length += 1
    return sentence


def getSeed(max_attempts=20):
    attempts = 0
    seed = random.choice(sets_of_k_words)
    while (attempts < max_attempts and
           (seed[0] == ',' or seed[0] == '—' or seed[0] == '.')):
        seed = random.choice(sets_of_k_words)
        attempts += 1
    return seed


def getContent():
    seed = getSeed(30)
    body = stochastic_chain(seed, seed_length=2, max_length=50, min_length=5)
    return body.capitalize()


if __name__ == "__main__":
    sent = getContent()
    print(sent)
