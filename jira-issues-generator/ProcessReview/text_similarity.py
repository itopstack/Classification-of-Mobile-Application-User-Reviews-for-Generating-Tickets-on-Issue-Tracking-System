import spacy
import nltk
import string
import re

nltk.download('punkt')
nlp = spacy.load('en_vectors_web_lg')

# Text pre-processing functions
stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
stopwords = nltk.corpus.stopwords.words('english')

def tokenize(text):
    return nltk.word_tokenize(text)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

def remove_stopwords(tokens):
    return [item for item in tokens if item not in stopwords]

def keep_alphabetic(tokens):
    return [item for item in tokens if item.isalpha()]

def reduce_lengthening(tokens):
    pattern = re.compile(r"(.)\1{2,}")
    return [pattern.sub(r"\1\1", item) for item in tokens]

'''lowercase, punctuation, remove stopwords, only alphabetic, reduce lengthening, stem'''
def normalize(text):
    lower_text_without_punctuation = text.lower().translate(remove_punctuation_map)
    return ' '.join(
                stem_tokens(
                reduce_lengthening(
                keep_alphabetic(
                remove_stopwords(
                tokenize(
                lower_text_without_punctuation))))))

def is_duplicate_review(sentence1, sentence2):
    threshold = 0.93
    doc1 = nlp(normalize(sentence1))
    doc2 = nlp(normalize(sentence2))
    similarity = doc1.similarity(doc2)
    return similarity >= threshold
