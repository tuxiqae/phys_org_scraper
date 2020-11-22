import re
import sys

import requests as r
import pandas as pd
from bs4 import BeautifulSoup as Soup

BASE_URL = "https://phys.org/physics-news/sort/date/3d/"


def get_by_url(url=None, params=None):
    if url is None:
        url = BASE_URL
    headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0"}

    response = r.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print("Could not reach: " + response.url +
              " status code: " + str(response.status_code))
        sys.exit(1)

    return response


def res_to_df(res):
    props = {
        "url": [],
        "title": [],
        # "category": []
    }

    doc = Soup(res.text, "lxml")

    while doc is not None:
        fetch_all_urls(doc, props["url"])
        doc = get_next_page(doc)

    for url in props["url"]:
        fetch_article_data(Soup(get_by_url(url).text, "lxml"), props)

    print(props)

    return pd.DataFrame(props)


def fetch_all_urls(page, urls):
    for article_elem in page.find_all("article", class_="sorted-article"):
        urls.append(article_elem.find("a", href=True, class_="news-link")["href"])

    return urls


def get_next_page(catalog):
    next_re = re.compile(r"^\s+»\s+$")
    if (next_page_elem := catalog.find("a", string=next_re)) is not None \
            and r"tab-index" not in next_page_elem.attrs:
        return Soup(get_by_url(BASE_URL + next_page_elem["href"]).text, "lxml")
    return None


def fetch_article_data(doc, props):
    props["title"].append(doc.title.text)


if __name__ == '__main__':
    df = res_to_df(get_by_url())
    print(df)
