import nltk.tokenize
from bs4 import BeautifulSoup
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import requests, re
import numpy as np

# Path to the local HTML file
file_path = '../jQuery/index.html'

stemmer = SnowballStemmer('english')
lemmet = WordNetLemmatizer()
url = ""
# Open and read the local HTML file
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all anchor tags in the HTML
anchor_tags = soup.find_all('a')

stop_words = stopwords.words("english")
# print(stop_words)

# Extract and print the href attribute from each anchor tag
for anchor_tag in anchor_tags:
    href = anchor_tag.get('href')
    tag_name = stemmer.stem(anchor_tag.getText())
    if href:
        if "term" in tag_name or "conditions" in tag_name or 't' in tag_name or 'c' in tag_name:
            url = href

all_words=[]

response = requests.get(url)

if response.status_code == 200:
    s_oup = BeautifulSoup(response.text, 'html.parser')
    body = s_oup.body.text
    exp = re.compile(r'[\n,&,(,)]')
    body = re.sub(exp, ' ', body)
    body = re.sub(' +', ' ', body)
    sentences = nltk.tokenize.sent_tokenize(body)
    for i in range(len(sentences)):
        words = nltk.tokenize.word_tokenize(sentences[i])
        all_words.extend(words)
        words = [lemmet.lemmatize(word, pos='n') for word in words if word not in set(stop_words)]
        sentences[i]=' '.join(words)
else:
    print("failure")
ignore_words = ['?', '.', '!']
all_words = [lemmet.lemmatize(w) for w in all_words if w not in ignore_words]

print(sentences)


# Alternatively, you can navigate to a specific link
# For example, if you want to navigate to the first link:
# first_link = anchor_tags[0].get('href')
# navigate_to_link(first_link)

