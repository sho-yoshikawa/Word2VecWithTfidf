from model import calcWord2Vec
import pandas as pd
import numpy as np

df = pd.read_csv("csv/scraping.csv")
restaurantName = df["name"]
restaurantLink = df["link"]

input_word = input("単語を入力してください。>>> ")
try:
    result = calcWord2Vec(input_word)
    word = result[0][0]
except KeyError:
    print("Error: KeyError")
    print("別の単語で試してみてください")
    exit()
print("word2vec result: ", word)

data = np.load("np/tfidf_3d.npy", allow_pickle=True)

matchs = []
for review_index, review in enumerate(data):
    nouns = [nounTfidf[0] for nounTfidf in review]
    tfidfs = [nounTfidf[1] for nounTfidf in review]
    match_indexs = [i for i, noun in enumerate(nouns) if noun == word]
    if len(match_indexs) > 0:
        match = [review_index, [review[i] for i in match_indexs]]
        matchs.append(match)
print(len(matchs), "件ヒットしました。")

high = 0
for match in matchs:
    tfidf = match[1][0][1]
    if high < tfidf:
        review_index = match[0]
        recommend_index = review_index
    # print(restaurantName[match[0] // 3])
print("====================")
print("1番のおすすめは、")
print("名前: ", restaurantName[recommend_index // 3])
print("リンク: ", restaurantLink[recommend_index // 3])
