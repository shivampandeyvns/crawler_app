import re
import string

import nltk

from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords

from nltk.stem import PorterStemmer

from nltk.stem import WordNetLemmatizer


class TextPreprocessor:

    def __init__(self):

        self.stop_words = set(stopwords.words("english"))

        self.stemmer = PorterStemmer()

        self.lemmatizer = WordNetLemmatizer()

    def clean(self,text):

        text=text.lower()

        text=re.sub(r"http\S+","",text)

        text=re.sub(r"\d+","",text)

        text=text.translate(
            str.maketrans(
                "",
                "",
                string.punctuation
            )
        )

        return text

    def tokenize(self,text):

        return word_tokenize(text)

    def remove_stopwords(self,tokens):

        return [

            w

            for w in tokens

            if w not in self.stop_words

        ]

    def stem(self,tokens):

        return [

            self.stemmer.stem(t)

            for t in tokens

        ]

    def lemmatize(self,tokens):

        return [

            self.lemmatizer.lemmatize(t)

            for t in tokens

        ]

    def preprocess(self,text):

        text=self.clean(text)

        tokens=self.tokenize(text)

        tokens=self.remove_stopwords(tokens)

        stems=self.stem(tokens)

        lemmas=self.lemmatize(tokens)

        return{

            "clean_text":" ".join(lemmas),

            "tokens":tokens,

            "stems":stems,

            "lemmas":lemmas

        }