import sys
sys.path.append('./ConnectJira')
sys.path.append('./ProcessReview')

import pandas as pd
import json
import doc2vec_classifier
import bug_classifier
import feature_classifier
import numpy as np
from utils import TextSelector, TfidfEmbeddingVectorizer, DenseTransformer, MeanEmbeddingVectorizer, NumberSelector
from text_summarizer import summarize
from create_issue import generate_ticket_on_jira
import datetime
import ast
from text_similarity import is_duplicate_review

is_mock = len(sys.argv) == 1 # if we execute main.py directly, the total number of sys argument will be 1. That means we are using mock mode.

def get_user_review():
    if is_mock:
        with open('./SampleData/mix_test.json') as data_file:
            json_data = json.load(data_file)

            # Assign platform and version
            result = []
            for data in json_data:
                data['platform'] = 'iOS'
                if not 'version' in data.keys():
                    data['version'] = '1.0'

                result.append(data)

            return result
    else:
        reviews = sys.argv[1]
        sys.stdout.flush()
        return ast.literal_eval(reviews)

# ================ Start from here ==================

# Get review
user_reviews = get_user_review()
data_frame = pd.DataFrame.from_dict(user_reviews, orient='columns')

# Keep only necessary fields and their values
data_frame = data_frame[['score', 'text', 'title', 'url', 'version', 'platform']]
data_frame = data_frame[data_frame.score.notnull() & data_frame.text.notnull() & data_frame.platform.notnull()]
data_frame.version.fillna('', inplace=True)

# Predict
bug_pred = bug_classifier.classify(data_frame.copy())
feature_pred = feature_classifier.classify(data_frame.copy())

data_frame['bug_predict'] = bug_pred
data_frame['feature_predict'] = feature_pred

# Filter `Not Bug` and `Not Feature` out
is_bug = data_frame['bug_predict'] != 'Not Bug'
is_feature = data_frame['feature_predict'] != 'Not Feature'
data_frame = data_frame[is_bug | is_feature]

# Create title from text summarization
data_frame['summarized_title'] = summarize(data_frame.text, expected_number_of_word=1)

# Assign current datetime
now = datetime.datetime.now()
formatted_date = now.strftime("%Y/%m/%d")
data_frame['created_date'] = formatted_date

# Generate ticket on JIRA and check duplicate reviews
created_user_reviews = []
for row in data_frame.itertuples(index=True, name='Pandas'):
    duplicate = False

    for created_review in created_user_reviews:
        duplicate = is_duplicate_review(sentence1=created_review.text, sentence2=row.text)
        if duplicate:
            break

    if not duplicate:
        generate_ticket_on_jira(row, base64Authentication=sys.argv[2])
        created_user_reviews.append(row)

print('\nCreate new ' + str(len(created_user_reviews)) + ' issues successfully! Please check your JIRA dashboard.')
