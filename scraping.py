from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service as cs

import pandas as pd

CHROMEDRIVER = "./chromedriver"
PURPLE = '\033[35m'
ENDC = '\033[0m'
TABELOG = "https://tabelog.com/tokyo/rstLst/izakaya/"

options = Options()
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')


chrome_service = cs.Service(executable_path=CHROMEDRIVER)
b = webdriver.Chrome(service=chrome_service, options=options)
# b.set_window_size(600, 600)


b.get(TABELOG)
restaurants = b.find_elements(By.CLASS_NAME, "list-rst__rst-name-target")
restaurantName = [restaurant.text for restaurant in restaurants]

restaurantLinks = [restaurant.get_attribute(
    "href") for restaurant in restaurants]

# for restaurant in restaurants:
#     print(PURPLE, restaurant.text, ENDC)

restaurantReview = []
for restaurantLink in restaurantLinks:
    print(restaurantLink)
    b.get(restaurantLink)
    reviews = b.find_elements(By.CLASS_NAME, "rstdtl-rvw__rvw-more")
    reviewLinks = [review.get_attribute("href") for review in reviews]
    for reviewLink in reviewLinks:
        b.get(reviewLink)
        reviewComment = b.find_element(
            By.CLASS_NAME, "rvw-item__rvw-comment")
        restaurantReview.append(reviewComment.text.replace(",", ""))

# print(len(restaurantName), len(restaurantReview))
df = pd.DataFrame(restaurantReview, columns=['review'])
df['name'] = pd.Series(restaurantName)
df['link'] = pd.Series(restaurantLinks)

df.to_csv('csv/scraping.csv')
b.quit()
