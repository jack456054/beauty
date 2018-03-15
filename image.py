import requests
from bs4 import BeautifulSoup
import re
import os

from urllib.request import urlretrieve
res = requests.get('https://www.ptt.cc/bbs/Beauty/M.1521033451.A.439.html')
bs4_html = BeautifulSoup(res.text, "html.parser")
titles = bs4_html.find_all("span", {"class": "article-meta-value"})
dirname = titles[2].text
imgs = bs4_html.find_all("a", {"href": re.compile("https://i.imgur.com/.*")})
count = 0
if not os.path.exists(dirname):
    os.mkdir(dirname)

for img in imgs:
    urlretrieve(img.text, "{}/{}/{}.jpg".format(os.getcwd(), dirname, count))
    count += 1
    print(img.text)
