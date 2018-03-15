# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import template
from bs4 import BeautifulSoup
import re
import os


def download_imgs(url):
    from urllib.request import urlretrieve
    res = requests.get('https://www.ptt.cc/{}'.format(url))
    bs4_html = BeautifulSoup(res.text, "html.parser")
    titles = bs4_html.find_all("span", {"class": "article-meta-value"})
    dirname = titles[2].text
    if '公告' in dirname:
        return 0
    dirname = dirname.replace("/", " ")
    imgs = bs4_html.find_all("a", {"href": re.compile('https://i.imgur.com/.*|https://imgur.com/.*')})
    count = 0
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    else:
        return 0
    for img in imgs:
        urlretrieve(img.text, "{}/{}/{}.jpg".format(os.getcwd(), dirname, count))
        count += 1


def input_value():
    input_msg = 'Pages(Default: 1): '
    page = input(input_msg)
    page = whether_help(page, input_msg)

    # Check whether valid input or exit or help
    while True:
        try:
            if not page:
                page = '1'
                print(page)
                break
            while int(page) <= 0:
                template.invalid_input_msg()
                page = input(input_msg)
                page = whether_help(page, input_msg)
            break

        # Check whether type correct
        except ValueError:
                template.invalid_input_msg()
                page = input(input_msg)
                page = whether_help(page, input_msg)

    # input_msg = 'Pushes(Default: 1): '
    # push = input(input_msg)
    # push = whether_help(push, input_msg)
    # while True:
    #     try:
    #         if push == '爆':
    #             push = '100'
    #             break
    #         elif not push:
    #             print('爆')
    #             push = '100'
    #             break
    #         while int(push) > 99 or int(push) < 0:
    #             template.invalid_input_msg()
    #             push = input(input_msg)
    #             push = whether_help(push, input_msg)
    #         else:
    #             return push
    #
    #     # Check whether type correct
    #     except ValueError:
    #         template.invalid_input_msg()
    #         push = input(input_msg)
    #         push = whether_help(push, input_msg)
    return page


# Check whether user needs help
def whether_help(user_input, input_msg):
    while user_input.lower() == 'help':
        template.instruction_browsepages()
        user_input = input(input_msg)
        whether_exit(user_input)
        if not user_input:
            return user_input
    whether_exit(user_input)
    return user_input


# Check whether user want to exit
def whether_exit(user_input):
    if user_input.lower() == 'exit':
        template.bye_msg()
        exit()


# Sending request to the website and if there is over18 website, answer "Yes"
def over18(current_page):

    # Sending request to the website
    res = requests.get(current_page)
    html_doc = res.text
    bs4_html = BeautifulSoup(html_doc, "html.parser")

    # If there is over18 website, answer "Yes"
    if bs4_html.find('div', {'class': 'over18-notice'}):
        payload = {
            'from': current_page,
            'yes': 'yes'
        }
        rs = requests.session()
        res = rs.post('https://www.ptt.cc/ask/over18', data=payload)
        res = rs.get(current_page)
        html_doc = res.text
        bs4_html = BeautifulSoup(html_doc, "html.parser")
    return bs4_html


def find_articles(page):

    # Check whether there is a age 18 verification
    older_page = None
    count_pages = 0
    # urls = []
    # articles_info = []
    category = 'beauty'
    current_page = ('https://www.ptt.cc/bbs/{}/index.html'.format(category))

    # Find push, titles, and urls in each page
    for i in range(1, page + 1):
        print("(Fetching page {:3}, please be patient.)".format(i))
        # Sending request and check over18 page
        bs4_html = over18(current_page)

        # Find titles and push
        articles = bs4_html.find_all("div", {"class": "r-ent"})
        for article in articles:
            # push_number = article.find("div", {"class": "nrec"})
            url = article.find("div", {"class": "title"}).find('a')
            if url:
                download_imgs(url.get('href'))

        # Get the url for the next page
        find_next_page = bs4_html.find_all('a', {"class": "btn wide"})
        for next_page in find_next_page:
            if next_page.text == "‹ 上頁":
                older_page = 'https://www.ptt.cc{}'.format(next_page.get('href'))

        # If not next page, print error message
        if not older_page:
            template.print_counts(count_pages)
            template.print_no_other_pages()
            return 0

        # Next page
        current_page = older_page
    print("Complete!!!!")


if __name__ == '__main__':
    page = input_value()
    find_articles(int(page))
