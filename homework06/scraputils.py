import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """Extract news from a given web page"""
    news_list = []

    # Извлекаем все строки с новостями
    rows = parser.select("tr.athing")

    for row in rows:
        title_tag = row.select_one("a.storylink")
        title = title_tag.get_text() if title_tag else "No title"
        url = title_tag['href'] if title_tag else "No link"
        score_tag = row.find_next_sibling("tr").select_one("span.score")
        score = int(score_tag.get_text().replace(" points", "")) if score_tag else 0
        user_tag = row.find_next_sibling("tr").select_one("a.hnuser")
        user = user_tag.get_text() if user_tag else "Anonymous"

        news_item = {
            "title": title,
            "url": url,
            "points": score,
            "user": user
        }

        news_list.append(news_item)

    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    morelink = parser.select_one("a.morelink")
    if morelink:
        return morelink['href']
    return None


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []

    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        if not next_page:
            break
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1

    return news
