import requests


def get_results(query):
    url = 'http://export.arxiv.org/api/query?search_query=all:' + query
    response = requests.get(url)
    print(response.text)


if __name__ == '__main__':
    get_results('autocalibration')
