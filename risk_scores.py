# import joblib, nltk
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer, WordNetLemmatizer
# from sklearn.feature_extraction.text import CountVectorizer
#
#
#
# model = joblib.load('model.joblib')
#
# def preprocess_function(text):
#     # Lowercasing
#     text = text.lower()
#
#     # Tokenization
#     tokens = nltk.tokenize.word_tokenize(text)
#
#     # Removing Punctuation
#     tokens = [token for token in tokens if token.isalnum()]
#
#     # Removing Stop Words
#     stop_words = set(stopwords.words('english'))
#     tokens = [token for token in tokens if token not in stop_words]
#
#     # Stemming
#     lemmatizer = WordNetLemmatizer()
#     tokens = [lemmatizer.lemmatize(token) for token in tokens]
#
#     # Join tokens back into a processed text
#     processed_text = ' '.join(tokens)
#
#     return processed_text
#
#
# def process_new_terms_and_conditions(new_terms_and_conditions):
#     # Preprocess the new terms and conditions
#     for sent in new_terms_and_conditions:
#         print(sent)
#         preprocessed_text = preprocess_function(sent)
#         # print(preprocessed_text)
#         new_data = [[1]]  # Replace '1' with the appropriate numerical value or features
#
#         # Make predictions using the loaded model
#         risk_class = model.predict(new_data)[0]
#
#         return risk_class
#
# # Example usage
# new_terms_and_conditions = """
# Acceptance of Terms: You accept these terms and conditions by visiting or using our website.
# Intellectual Property: The material, pictures, graphics, and logos on this website are all the owner's and are covered by copyright laws.
# Website Use: You may only use this website in line with these terms and conditions and for reasons that are permitted by law.
# Disclaimer: The material on this website is only provided for general informational purposes and is not intended to be advice on any professional, financial, or other problems.We make no representations or warranties of any kind, express or implied, as to the completeness, accuracy, reliability, suitability, or availability for any purpose of the website or related graphics given on the website.
# Limitation of Liability: We expressly disclaim all liability for any direct, indirect, incidental, special, or consequential damages that may arise from the use of or the inability to use this website or the information, goods, services, or associated visuals provided on the website.
# Links to Other Websites: We have no control over the links that may appear on our website leading to other websites.Any connected website's practices, privacy policies, or content are not our responsibility.
# Privacy Statement: We take seriously our responsibility to secure your personal information.
# Governing Law: Without regard to any considerations of conflict of law, these terms and conditions shall be governed by and construed in accordance with the laws of [State/Country].
# Terms and Conditions Changes: We have the right to make changes to these terms and conditions at any time and without prior notice.
# """
#
# # Process the new terms and conditions
# risk_class = process_new_terms_and_conditions(new_terms_and_conditions)
#
# # Print the result
# print("Risk Class:", risk_class)
#

import re
import nltk.tokenize
import pandas as pd
import joblib

from train import calculate_risk_score, exp

# Load the trained model
classifier = joblib.load('model.joblib')

# New terms and conditions
# new_sample_terms_and_conditions = """
# Acceptance of Terms: You accept these terms and conditions by visiting or using our website.
# Intellectual Property: The material, pictures, graphics, and logos on this website are all the owner's and are covered by copyright laws.
# Website Use: You may only use this website in line with these terms and conditions and for reasons that are permitted by law.
# Disclaimer: The material on this website is only provided for general informational purposes and is not intended to be advice on any professional, financial, or other problems.We make no representations or warranties of any kind, express or implied, as to the completeness, accuracy, reliability, suitability, or availability for any purpose of the website or related graphics given on the website.
# Limitation of Liability: We expressly disclaim all liability for any direct, indirect, incidental, special, or consequential damages that may arise from the use of or the inability to use this website or the information, goods, services, or associated visuals provided on the website.
# Links to Other Websites: We have no control over the links that may appear on our website leading to other websites.Any connected website's practices, privacy policies, or content are not our responsibility.
# Privacy Statement: We take seriously our responsibility to secure your personal information.
# Governing Law: Without regard to any considerations of conflict of law, these terms and conditions shall be governed by and construed in accordance with the laws of [State/Country].
# Terms and Conditions Changes: We have the right to make changes to these terms and conditions at any time and without prior notice.
# Protecting company ensuring understand issue like liability integral component keeping SaaS functioning.
# It 's important Privacy Policy place collect personal information like name email address payment information.
# """
def analyzing_terms_and_conditions(new_terms_and_conditions):
    new_terms_and_conditions = re.sub(exp, '', new_terms_and_conditions)
    sentences = new_terms_and_conditions.split('.')

    term_risk_dict = {}

    for sent in nltk.tokenize.sent_tokenize(new_terms_and_conditions):
        # print(sent)
        risk_score = calculate_risk_score(sent)
        term_risk_dict[sent] = risk_score
        # print("Risk Score:", risk_score)

    # Predict risk classes using the trained model
    predictions = classifier.predict(pd.DataFrame({'risk_score': term_risk_dict.values()})[['risk_score']])

    result_dict={}
    # Display the results
    for term, prediction in zip(term_risk_dict.keys(), predictions):
        result_dict[term]=prediction
    return result_dict