from gensim import corpora
from gensim import models
from pprint import pprint  # オブジェクトを整えて表示するライブラリ. gensimのtfidf計算には不要
import pandas as pd
import numpy as np

df = pd.read_csv("csv/preprocessTextneologd_2d.csv")

data = [[y for y in x if isinstance(y, str)] for x in df.values.tolist()]

# 単語->id変換の辞書作成
dictionary = corpora.Dictionary(data)
# pprint(dictionary.token2id)

# textsをcorpus化
corpus = list(map(dictionary.doc2bow, data))
# print(dictionary.doc2bow(text[0]))
# pprint(corpus)

# tfidf modelの生成
test_model = models.TfidfModel(corpus)

# corpusへのモデル適用
corpus_tfidf = test_model[corpus]

# for doc in corpus_tfidf:
#     print(doc)


# id->単語へ変換
texts_tfidf = []  # id -> 単語表示に変えた文書ごとのTF-IDF
for doc in corpus_tfidf:
    text_tfidf = []
    for word in doc:
        text_tfidf.append([dictionary[word[0]], word[1]])
    texts_tfidf.append(text_tfidf)

# for text in texts_tfidf:
#     print(text)

# will be warning.
na = np.array(texts_tfidf)
np.save("np/tfidf_3d.npy", na)

# for text in texts_tfidf:
#     print(text)
