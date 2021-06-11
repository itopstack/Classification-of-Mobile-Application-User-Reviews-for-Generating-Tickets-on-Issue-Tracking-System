import pandas as pd
import numpy as np
import nltk
import re
import heapq

stopwords = nltk.corpus.stopwords.words('english')

def count_word_frequencies(formatted_text):
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    return word_frequencies

def count_sentence_scores(sentence_list, word_frequencies):
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    return sentence_scores

def summarize(data_frame_column, expected_number_of_word):
    summaries = []

    for raw_text in data_frame_column:
        # Removing special characters and digits
        formatted_text = re.sub('[^a-zA-Z]', ' ', raw_text)
        formatted_text = re.sub(r'\s+', ' ', formatted_text)

        sentence_list = nltk.sent_tokenize(raw_text)
        word_frequencies = count_word_frequencies(formatted_text)
        maximum_frequncy = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

        sentence_scores = count_sentence_scores(sentence_list, word_frequencies)

        summary_sentences = heapq.nlargest(expected_number_of_word, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(summary_sentences)
        summaries.append(summary)

    return summaries
