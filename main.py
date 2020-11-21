import requests as r
import pandas as pd
from bs4 import BeautifulSoup as Soup


def get_by_url(url, headers, params):
    response = r.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print("Could not reach: " + response.url + " status code: " + str(response.status_code))
        exit(1)

    return response


if __name__ == '__main__':
    URL = "https://phys.org/physics-news/sort/date/1d/"
    params = {}
    headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0"}
    res = get_by_url(URL, headers, params)