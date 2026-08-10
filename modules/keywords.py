from sklearn.feature_extraction.text import CountVectorizer


class KeywordExtractor:

    def extract(self,text,n=10):

        vectorizer=CountVectorizer(

            stop_words="english"

        )

        matrix=vectorizer.fit_transform([text])

        words=vectorizer.get_feature_names_out()

        freq=matrix.toarray().sum(axis=0)

        pairs=list(zip(words,freq))

        pairs=sorted(

            pairs,

            key=lambda x:x[1],

            reverse=True

        )

        return pairs[:n]