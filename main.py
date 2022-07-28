from flask import Flask,request,jsonify
import json
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import spacy
nlp = spacy.load('en_core_web_sm')

response = 'before'
result = {}
app = Flask(__name__)

@app.route('/review',methods=['GET','POST'])

def uploadUsreReview():
    global response
    if(request.method=='POST'):
        request_data = request.data
        request_data = json.loads(request_data.decode('utf-8'))
        review = request_data['review']
        # tokenization
        lower = review.lower()
        words = word_tokenize(lower, "english")
        # remove punctuation
        # def isCountry(text):
        #  count = 0
        #  flag = 0
        #  for letter in text:
        #   count+=1
        #   if( count == 1 and letter == "."):
        #    print(text)
        #    flag=1
        #  return flag

        text_after_remove_punc = []

        def removePunc(words):
            removed = []
            for word in words:
                for letter in word:
                    if letter in string.punctuation:
                        word = word.replace(letter, "")
                removed.append(word)
            return removed

        text_after_remove_punc = removePunc(words)
        print(text_after_remove_punc)
        valueToBeRemoved = ""
        # remove all empty string
        try:
            while True:
                text_after_remove_punc.remove(valueToBeRemoved)
        except ValueError:
            pass

        # remove stop words
        text_after_stop_words = []
        for word in text_after_remove_punc:
            if word not in set(stopwords.words('english')):
                text_after_stop_words.append(word)

        print(text_after_stop_words)
        # convert to stemming text
        ps = PorterStemmer()
        stem_text = []
        for word in text_after_stop_words:
            stem_text.append(ps.stem(word))
        print(stem_text)

        ################################
        # convert to lemmatization
        # Function to convert
        def listToString(s):
            str1 = ""
            for ele in s:
                str1 += ele + ' '
            return str1

        text_lemma = []
        doc1 = nlp(listToString(text_after_stop_words))
        for token in doc1:
            text_lemma.append(token.lemma_)

        # sentiment analysis
        finalVal = ""

        result=sentimentAnalyze(finalVal,text_after_remove_punc)

        return jsonify(result)

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele + ' '
    return str1
def sentimentAnalyze(finalVal,text_after_remove_punc):
    score = SentimentIntensityAnalyzer().polarity_scores(listToString(text_after_remove_punc))
    print(score)
    if score['pos'] > score['neg']:
        finalVal = 'Positive'
        print('Positive')
    elif score['pos'] < score['neg']:
        finalVal = 'Negative'
        print('negative')
    else:
        finalVal = 'Equal Article'
        print('equal article')
    return {'positive':score['pos'],
            'negative':score['neg']
            }


if __name__ == '__main__':
    app.run(debug=True, port=7070)