import pandas as pd
import re
import MeCab

IPADIC_DICT = "-d /Users/sho/Homebrew/lib/mecab/dic/ipadic"
IPADIC_NEOLOGD_DICT = "-d /Users/sho/Homebrew/lib/mecab/dic/mecab-ipadic-neologd"
# need export, set env like this
# MECABRC = "/Users/sho/Homebrew/lib/mecab/dic/mecab-ipadic-neologd"

df = pd.read_csv("csv/scraping.csv")

names = df['name'].tolist()
reviews = df['review'].tolist()


def preprocess(text):
    text = text.replace("\n", "")
    text = text.replace("！", "")
    text = text.replace("？", "")
    text = text.replace("!", "")
    text = text.replace("?", "")
    text = re.sub("\(.*\)", "", text)
    text = re.sub("（.*）", "", text)
    text = re.sub("[0-9]*円", "", text)
    text = re.sub(
        "(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", "", text)
    return text


def makePreprocessCSV(reviews):
    reviews = [preprocess(review) for review in reviews]
    mecab = MeCab.Tagger(IPADIC_NEOLOGD_DICT)
    reviewNoun_2d = []
    for review in reviews:
        parse = mecab.parse(review)
        parse = parse.splitlines()[:-1]
        review = [line.split()[0] for line in parse if "名詞" in line.split()[
            1] and re.match(r"[ぁ-ん]|[0-9]|[０-９]|[a-z]|[A-Z]", line.split()[0]) is None]
        reviewNoun_2d.append(review)
    reviewNoun = [Noun for review in reviewNoun_2d for Noun in review]
    df = pd.DataFrame(reviewNoun, columns=["noun"])
    df.to_csv("csv/preprocessTextNeologd.csv")
    df_2d = pd.DataFrame(reviewNoun_2d)
    df_2d.to_csv("csv/preprocessTextNeologd_2d.csv")


def MecabAnalyzer(reviews):
    mecab = MeCab.Tagger(IPADIC_NEOLOGD_DICT)
    parse = mecab.parse(reviews)
    parse = parse.splitlines()[:-1]
    review = [line.split()[0] for line in parse if "名詞" in line.split()[
        1] and re.match(r"[ぁ-ん]|[0-9]|[０-９]|[a-z]|[A-Z]", line.split()[0]) is None]
    return review


# def myMecabAnalyzer(reviews):
#     mecab = MeCab.Tagger(IPADIC_DICT)
#     parse = mecab.parse(reviews)
#     parse = parse.splitlines()[:-1]
#     review = [line.split()[0] for line in parse if "名詞" in line.split()[
#         1] and re.match(r"[ぁ-ん]|[0-9]|[０-９]|[a-z]|[A-Z]", line.split()[0]) is None]
#     return review

if __name__ == "__main__":
    makePreprocessCSV(reviews)
