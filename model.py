import pandas as pd
from gensim.models import Word2Vec


def makeModel():
    df_processTextNeologd = pd.read_csv("csv/preprocessTextNeologd.csv")
    noun = df_processTextNeologd["noun"].tolist()
    model = Word2Vec(sentences=[noun], min_count=1, window=10)
    model.save("model/tabelog.model")
    model.wv.save_word2vec_format("model/tabelog.vec", binary=False)


def calcWord2Vec(word):
    model = Word2Vec.load("model/tabelog.model")
    ret = model.wv.most_similar(positive=[word])
    return ret


makeModel()
