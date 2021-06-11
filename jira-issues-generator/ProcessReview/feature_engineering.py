import nltk
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import gensim
from gensim.models import Word2Vec
import textblob
import numpy as np

stopwords = nltk.corpus.stopwords.words('english')
wv = gensim.models.KeyedVectors.load_word2vec_format("./ClassifierModel/GoogleNews-vectors-negative300.bin.gz", binary=True)
wv.init_sims(replace=True)

def tokenize(text):
    return nltk.word_tokenize(text)

def remove_stopwords(tokens):
    return [item for item in tokens if item not in stopwords]

def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(item) for item in tokens]

def sentiment_analyzer_scores(sentence):
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(sentence)
    return score['compound']

def word_averaging(wv, words):
    all_words, mean = set(), []

    for word in words:
        if isinstance(word, np.ndarray):
            mean.append(word)
        elif word in wv.vocab:
            mean.append(wv.vectors_norm[wv.vocab[word].index])
            all_words.add(wv.vocab[word].index)

    if not mean:
        return np.zeros(wv.vector_size,)

    mean = gensim.matutils.unitvec(np.array(mean).mean(axis=0)).astype(np.float32)
    return mean

def word_averaging_list(text_list):
    return np.vstack([word_averaging(wv, post) for post in text_list])

def w2v_tokenize_text(text):
    tokens = []
    for sent in nltk.sent_tokenize(text, language='english'):
        for word in nltk.word_tokenize(sent, language='english'):
            if len(word) < 2:
                continue
            tokens.append(word)
    return tokens

# function to check and get the part of speech tag count of a words in a given sentence
def check_pos_tag(x, flag):
    pos_family = {
                    'noun': ['NN', 'NNS', 'NNP', 'NNPS'],
                    'pron': ['PRP', 'PRP$', 'WP', 'WP$'],
                    'verb': ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],
                    'adj':  ['JJ', 'JJR', 'JJS'],
                    'adv': ['RB', 'RBR', 'RBS', 'WRB']
                }

    cnt = 0
    try:
        wiki = textblob.TextBlob(x)
        for tup in wiki.tags:
            ppo = list(tup)[1]
            if ppo in pos_family[flag]:
                cnt += 1
    except:
        pass
    return cnt

def compute_pos_text(data_frame, tag, text):
    new_data_frame = data_frame
    new_data_frame[tag] = new_data_frame[text].apply(lambda x: check_pos_tag(x, tag))
    return new_data_frame
