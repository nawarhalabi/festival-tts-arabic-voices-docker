from keras.models import load_model
import numpy as np
import pickle as pkl
import tensorflow as tf
import re

CONSTANTS_PATH = './constants'

with open(CONSTANTS_PATH + '/ARABIC_LETTERS_LIST.pickle', 'rb') as file:
    ARABIC_LETTERS_LIST = pkl.load(file)
with open(CONSTANTS_PATH + '/DIACRITICS_LIST.pickle', 'rb') as file:
    DIACRITICS_LIST = pkl.load(file)
with open(CONSTANTS_PATH + '/RNN_BIG_CHARACTERS_MAPPING.pickle', 'rb') as file:
    CHARACTERS_MAPPING = pkl.load(file)
with open(CONSTANTS_PATH + '/RNN_CLASSES_MAPPING.pickle', 'rb') as file:
    CLASSES_MAPPING = pkl.load(file)
with open(CONSTANTS_PATH + '/RNN_REV_CLASSES_MAPPING.pickle', 'rb') as file:
    REV_CLASSES_MAPPING = pkl.load(file)
    
punc = re.compile('([\\.,،:;\\[\\]\\(\\)\\{\\}«؛»])')
not_diac = re.compile('([^' + ''.join(CLASSES_MAPPING)[:-20] + '])')
    
def to_one_hot(data, size):
    one_hot = list()
    for elem in data:
        cur = [0] * size
        cur[elem] = 1
        one_hot.append(cur)
    return one_hot

def remove_diacritics(data_raw):
    return data_raw.translate(str.maketrans('', '', ''.join(DIACRITICS_LIST)))

def map_data(data_raw):
    X = list()
    Y = list()
    
    m = 0
    
    for line in data_raw:        
        x = [CHARACTERS_MAPPING['<SOS>']]
        y = [CLASSES_MAPPING['<SOS>']]
        
        splits = re.split(not_diac, line)
        x.extend([CHARACTERS_MAPPING.get(i, CHARACTERS_MAPPING['.']) for i in splits[1::2]])
        y.extend([CLASSES_MAPPING.get(i, CLASSES_MAPPING['']) for i in splits[2::2]])
        
        assert(len(x) == len(y))
        
        x.append(CHARACTERS_MAPPING['<EOS>'])
        y.append(CLASSES_MAPPING['<EOS>'])
        
        y = to_one_hot(y, len(CLASSES_MAPPING))
        
        X.append(x)
        Y.append(y)
        
        if len(x) > m:
            m = len(x)
    
    
    for i in range(len(X)):
        X[i].extend([CHARACTERS_MAPPING['<PAD>']] * (m - len(X[i])))
        Y[i].extend(to_one_hot([CLASSES_MAPPING['<PAD>']] * (m - len(Y[i])), len(CLASSES_MAPPING)))
    
    X = np.asarray(X)
    Y = np.asarray(Y)
    
    return X, Y    

def predict(line, model):
    line = punc.sub(string=line, repl='\n')
    lines = line.split('\n')
    X, _ = map_data(lines)
    predictions = model.predict(X)
    
    output = []
    for line, prediction_line in zip(lines, predictions):
        for char, prediction in zip(line, prediction_line[1:-1]):
            output.append(char)

            if char not in ARABIC_LETTERS_LIST:
                continue

            if '<' in REV_CLASSES_MAPPING[np.argmax(prediction)]:
                continue

            output += REV_CLASSES_MAPPING[np.argmax(prediction)]
        output.append('\n')

    return ''.join(output)

