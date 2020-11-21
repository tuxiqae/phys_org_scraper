import requests as r
import pandas as pd
from bs4 import BeautifulSoup as Soup


def get_by_url(url, params):
    headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0"}
    response = r.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print("Could not reach: " + response.url + " status code: " + str(response.status_code))
        exit(1)

    return response


def fetch_res():
    url = "https://phys.org/physics-news/sort/date/1d/"
    params = {}
    return get_by_url(url, params)


def res_to_df(res):
    props = {
        "title": [],
        "url": [],
        # "category": []
    }

    for article_elem in Soup(res.text, "lxml").find_all("article", class_="sorted-article"):
        populate_urls(article_elem, props)

    for url in props["url"]:
        res = Soup(get_by_url(url, {}).text, "lxml")
        print(url)  # TODO: remove

        props["title"].append(res.title.text)
        # print(res.find("a", href=True, class_="article-byline__link").text)

    return pd.DataFrame(props)


def populate_urls(elem, articles):
    title = elem.find("a", href=True, class_="news-link")
    articles["url"].append(title["href"])


if __name__ == '__main__':
    df = res_to_df(fetch_res())
    print(df)
