#!/usr/bin/env python3


import sys
import requests
import re


CRED = '\033[91m'
CGREEN = '\33[32m'
CYELLOW = '\33[33m'
CBLUE = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE = '\33[36m'
CWHITE = '\33[37m'
CEND = '\033[0m'


def get_results(query, max_results):
    url = 'http://export.arxiv.org/api/query?search_query=all:' + query \
          + '&start=0&max_results=' + max_results + '&sortBy=submittedDate'
    response = requests.get(url)
    # print(response.text)
    title_re = re.compile('<title>[\s\S]*?</title>')
    date_re = re.compile('<published>[\s\S]*?</published>')
    link_re = re.compile('<link title="pdf"[\s\S]*?rel="related"')
    titles = []
    dates = []
    links = []
    for title in title_re.finditer(response.text):
        titles.append(response.text[title.span()[0]+7:title.span()[1]-8])
    for date in date_re.finditer(response.text):
        dates.append(response.text[date.span()[0]+11:date.span()[1]-22])
    for link in link_re.finditer(response.text):
        links.append(response.text[link.span()[0]+len("<link title='pdf' href='"):link.span()[1]-15])

    assert(len(titles) == len(dates) == len(links))

    for i in range(len(titles)):
        print(CYELLOW + titles[i] + '\n' + dates[i] + '\n' + links[i] + CEND + '\n')


if __name__ == '__main__':
    get_results(sys.argv[1], sys.argv[2])
