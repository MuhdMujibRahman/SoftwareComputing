
import string
import numpy as np

training_data_file = 'eminem_songs_lyrics.txt'

def remove_punctuation(sentence):
    return sentence.translate(str.maketrans('','', string.punctuation))

def add2dict(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(value)

def list2probabilitydict(given_list):
    probability_dict = {}
    given_list_length = len(given_list)
    for item in given_list:
        probability_dict[item] = probability_dict.get(item, 0) + 1
    for key, value in probability_dict.items():
        probability_dict[key] = value / given_list_length
    return probability_dict

initial_word = {}
second_word = {}
transitions = {}


def train_markov_model():
    for line in open(training_data_file):
        tokens = remove_punctuation(line.rstrip().lower()).split()
        tokens_length = len(tokens)
        for i in range(tokens_length):
            token = tokens[i]
            if i == 0:
                initial_word[token] = initial_word.get(token, 0) + 1
            else:
                prev_token = tokens[i - 1]
                if i == tokens_length - 1:
                    add2dict(transitions, (prev_token, token), 'END')
                if i == 1:
                    add2dict(second_word, prev_token, token)
                else:
                    prev_prev_token = tokens[i - 2]
                    add2dict(transitions, (prev_prev_token, prev_token), token)

    # Normalize the distributions
    initial_word_total = sum(initial_word.values())
    for key, value in initial_word.items():
        initial_word[key] = value / initial_word_total

    for prev_word, next_word_list in second_word.items():
        second_word[prev_word] = list2probabilitydict(next_word_list)

    for word_pair, next_word_list in transitions.items():
        transitions[word_pair] = list2probabilitydict(next_word_list)

    print('Training successful.')


train_markov_model()
print(initial_word)
print(second_word)

def sample_word(dictionary):
    p0 = np.random.random()
    cumulative = 0
    for key, value in dictionary.items():
        cumulative += value
        if p0 < cumulative:
            return key
    assert(False)

number_of_sentences = 1

def generate(word):
    try:

        for i in range(number_of_sentences):
            sentence = []
            # Initial word
            inputw=word
            word0 = inputw.casefold()
            sentence.append(word0)
            # Second words
            word1 = sample_word(second_word[word0])
            sentence.append(word1)
            print(' '.join(sentence))

    except:
        print("dsddasdasdasda")



while(True):
    try:
        word = input("Enter input: ")
        generate(word)
    except:
        KeyboardInterrupt


