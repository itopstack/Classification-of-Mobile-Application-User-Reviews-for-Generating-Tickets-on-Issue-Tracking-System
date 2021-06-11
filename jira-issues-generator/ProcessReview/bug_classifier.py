from feature_engineering import tokenize, lemmatize, remove_stopwords, w2v_tokenize_text, word_averaging_list
import pandas as pd
import pickle

def classify(user_reviews_data_frame):
    classifier_model = pickle.load(open("./ClassifierModel/w2v_stopwords_lemmatization_voting", "rb"))
    user_reviews_data_frame['stopwords_removal_lemmatization'] = user_reviews_data_frame['text'].apply(lambda text: ' '.join(lemmatize(remove_stopwords(tokenize(text)))))
    test_tokenized = user_reviews_data_frame.apply(lambda r: w2v_tokenize_text(r['stopwords_removal_lemmatization']), axis=1).values
    X_test_word_average = word_averaging_list(test_tokenized)
    y_pred = classifier_model.predict(X_test_word_average)
    return y_pred
