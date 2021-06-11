import pandas as pd
import pickle
from feature_engineering import tokenize, lemmatize, compute_pos_text

def classify(user_reviews_data_frame):
    classifier_model = pickle.load(open("./ClassifierModel/lemmatization_pos_extra_tree", "rb"))
    user_reviews_data_frame['lemmatized_comment'] = user_reviews_data_frame['text'].apply(lambda text: ' '.join(lemmatize(tokenize(text))))

    user_reviews_data_frame['noun'] = compute_pos_text(user_reviews_data_frame, 'noun', 'lemmatized_comment')
    user_reviews_data_frame['pron'] = compute_pos_text(user_reviews_data_frame, 'pron', 'lemmatized_comment')
    user_reviews_data_frame['verb'] = compute_pos_text(user_reviews_data_frame, 'verb', 'lemmatized_comment')
    user_reviews_data_frame['adj'] = compute_pos_text(user_reviews_data_frame, 'adj', 'lemmatized_comment')
    user_reviews_data_frame['adv'] = compute_pos_text(user_reviews_data_frame, 'adv', 'lemmatized_comment')

    y_pred = classifier_model.predict(user_reviews_data_frame)
    return y_pred
