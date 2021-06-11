from tqdm import tqdm
tqdm.pandas(desc="progress-bar")
from gensim.models import Doc2Vec
import gensim
from gensim.models.doc2vec import TaggedDocument
import pandas as pd
import numpy as np
from sklearn import utils
import pickle
from feature_engineering import tokenize, remove_stopwords, lemmatize

def label_sentences(corpus, label_type):
    """
    Gensim's Doc2Vec implementation requires each document/paragraph to have a label associated with it.
    We do this by using the TaggedDocument method. The format will be "TRAIN_i" or "TEST_i" where "i" is
    a dummy index of the post.
    """
    labeled = []
    for i, v in enumerate(corpus):
        label = label_type + '_' + str(i)
        labeled.append(TaggedDocument(v.split(), [label]))
    return labeled

def get_vectors(model, corpus_size, vectors_size, vectors_type):
    """
    Get vectors from trained doc2vec model
    :param doc2vec_model: Trained Doc2Vec model
    :param corpus_size: Size of the data
    :param vectors_size: Size of the embedding vectors
    :param vectors_type: Training or Testing vectors
    :return: list of vectors
    """
    vectors = np.zeros((corpus_size, vectors_size))
    for i in range(0, corpus_size):
        prefix = vectors_type + '_' + str(i)
        vectors[i] = model.docvecs[prefix]
    return vectors

def build_doc2vec_model(input_data_array):
    series = pd.Series(input_data_array)

    X_test = label_sentences(series, 'Test')
    model_dbow = Doc2Vec(dm=0, vector_size=300, negative=5, min_count=1, alpha=0.065, min_alpha=0.065)
    model_dbow.build_vocab([x for x in tqdm(X_test)])

    for epoch in range(30):
        model_dbow.train(utils.shuffle([x for x in tqdm(X_test)]), total_examples=len(X_test), epochs=1)
        model_dbow.alpha -= 0.002
        model_dbow.min_alpha = model_dbow.alpha

    return get_vectors(model_dbow, len(X_test), 300, 'Test')

def classify(data_frame):
    # Load classifier models
    bug_classifier_model = pickle.load(open("./ClassifierModel/doc2vec_bug_classifier.pkl", "rb"))
    feature_classifier_model = pickle.load(open("./ClassifierModel/doc2vec_feature_classifier.pkl", "rb"))

    # Predict Bug
    raw_texts = data_frame['text'].values
    stopword_removed_test_data = map(lambda text: ' '.join(remove_stopwords(tokenize(text))), raw_texts)
    stopword_removed_test_vector = build_doc2vec_model(stopword_removed_test_data)
    y_pred_from_bug_classifier_model = bug_classifier_model.predict(stopword_removed_test_vector)

    # Predict Feature
    stopword_removed_lemmatized_test_data = map(lambda text: ' '.join(lemmatize(remove_stopwords(tokenize(text)))), raw_texts)
    stopword_removed_lemmatized_test_vector = build_doc2vec_model(stopword_removed_lemmatized_test_data)
    y_pred_from_feature_classifier_model = feature_classifier_model.predict(stopword_removed_lemmatized_test_vector)

    return y_pred_from_bug_classifier_model, y_pred_from_feature_classifier_model
