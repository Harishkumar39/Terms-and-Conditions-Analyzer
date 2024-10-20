import re

import nltk.tokenize
import pandas as pd

from sklearn.svm import SVC

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import joblib
from sklearn.metrics import accuracy_score, classification_report


# Define risk factors and corresponding scores
risk_factors = {
        'Acceptance of Terms': 1,
        'Intellectual Property': 2,
        'Use of Website': 1,
        'Disclaimer': 3,
        'Limitation of Liability': 4,
        'Links to Third-Party Websites': 3,
        'Privacy Policy': 2,
        'Governing Law': 2,
        'Changes to Terms and Conditions': 2,
        'Privacy': 1,
        'Policy': 1,
        'Prohibited Uses': 4,
        'Promotions': 2,
        'Proprietary Rights': 3,
        'Quality Refund': 3,
        'Registration': 1,
        'Remedies': 2,
        'Representations': 3,
        'Restrictions': 3,
        'Severability': 1,
        'Sharing of Information': 2,
        'Suspension': 4,
        'Taxes': 3,
        'Termination': 4,
        'Third-Party Services': 3,
        'Trademarks': 2,
        'Transparency': 1,
        'Unsolicited Ideas': 4,
        'User-Generated Content': 3,
        'Use of Website Validity': 1,
        'Verification': 2,
        'Viruses': 4,
        'Waiver': 3
    }





def calculate_risk_score(terms_and_conditions):

    total_score = 0
    # Check for the presence of each risk factor in the terms and conditions
    for factor, score in risk_factors.items():
        if factor.lower() in terms_and_conditions.lower():
            total_score += score

    return (total_score*len(risk_factors))/len(nltk.tokenize.word_tokenize(terms_and_conditions))


exp = re.compile(r'[\n]')

# Provided terms and conditions
sample_terms_and_conditions = """
Acceptance of Terms: You accept these terms and conditions by visiting or using our website. 
Intellectual Property: The material, pictures, graphics, and logos on this website are all the owner's and are covered by copyright laws. 
Website Use: You may only use this website in line with these terms and conditions and for reasons that are permitted by law. 
Disclaimer: The material on this website is only provided for general informational purposes and is not intended to be advice on any professional, financial, or other problems.We make no representations or warranties of any kind, express or implied, as to the completeness, accuracy, reliability, suitability, or availability for any purpose of the website or related graphics given on the website. 
Limitation of Liability: We expressly disclaim all liability for any direct, indirect, incidental, special, or consequential damages that may arise from the use of or the inability to use this website or the information, goods, services, or associated visuals provided on the website. 
Links to Other Websites: We have no control over the links that may appear on our website leading to other websites.Any connected website's practices, privacy policies, or content are not our responsibility. 
Privacy Statement: We take seriously our responsibility to secure your personal information. 
Governing Law: Without regard to any considerations of conflict of law, these terms and conditions shall be governed by and construed in accordance with the laws of [State/Country]. 
Terms and Conditions Changes: We have the right to make changes to these terms and conditions at any time and without prior notice. 
"""

# text = """Automatic summarization is the process of reducing a text document with a computer program in order to create a summary that retains the most important points of the original document. As the problem of information overload has grown, and as the quantity of data has increased, so has interest in automatic summarization. Technologies that can make a coherent summary take into account variables such as length, writing style and syntax. An example of the use of summarization technology is search engines such as Google. Document summarization is another."""

sample_terms_and_conditions = re.sub(exp, '', sample_terms_and_conditions)

term_risk_dict = {}
for sent in nltk.tokenize.sent_tokenize(sample_terms_and_conditions):
    # print(sent)
    risk_score= calculate_risk_score(sent)
    term_risk_dict[sent] = risk_score
    print("Risk Score:", risk_score)

risk_score_classes = {
    'Very Risky': lambda x: x > 2.5,
    'Risky': lambda x: 1.5 <= x <= 2.5,
    'Not Risky': lambda x: x < 1.5
}

risk_class = (next(cls for cls, condition in risk_score_classes.items() if condition(scores)) for term,scores in term_risk_dict.items())

risk_list = []

for risk_cls in risk_class:
    risk_list.append(risk_cls)

terms_class_dict = {}

for cls, terms in zip(risk_list, term_risk_dict.keys()):
    terms_class_dict[terms] = cls
# for term, cls in terms_class_dict.items():
#     print(f'{cls}\t{term}')



data = {'risk_score': term_risk_dict.values(), 'risk_class': risk_list}
df = pd.DataFrame(data)
# print(df)


train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# classifier = LogisticRegression(max_iter=1000)
classifier = SVC(kernel='linear')
classifier.fit(train_df[['risk_score']], train_df['risk_class'])

joblib.dump(classifier, 'model.joblib')

predictions = classifier.predict(test_df[['risk_score']])

# print(predictions)
accuracy = accuracy_score(test_df['risk_class'], predictions)
classification_report_str = classification_report(test_df['risk_class'], predictions,zero_division=1)

print("Accuracy:", accuracy)
print("\nClassification Report:\n", classification_report_str)



"""    
Group: Very risky
- Disclaimer: Not intended as legal, financial, or other professional advice.

Group: Risky
- Limitation of Liability: Not liable for any damages arising out of the use or inability to use the website.
- Links to Third-Party Websites: Not responsible for the content, privacy policies, or practices of linked websites.

Group: Not risky
- Acceptance of Terms: Agree to be bound by these terms and conditions.
- Intellectual Property: Content on the website is the property of the website owner.
- Use of Website: Use the website only for lawful purposes and in accordance with these terms and conditions.
- Privacy Policy: Committed to protecting personal information.
- Governing Law: Terms and conditions governed by the laws of [State/Country].
- Changes to Terms and Conditions: Reserve the right to modify terms and conditions without prior notice.
"""