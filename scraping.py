import json
import time
from config import *
import requests
from bs4 import BeautifulSoup
from bot_chanel import send_telegram


def check_update_news():

    login = USER_LOGIN
    password = USER_PASSWORD
    login_url = "account/login"
    url_login = URL+login_url
    payload = {"form_type": "customer_login",
               "customer[email]": login,
               "customer[password]": password
               }
    session = requests.Session()
    session.post(url_login, data=payload)

    with open("news_dict.json") as file:
        all_news = json.load(file)

    while True:
        try:
            headers = {
                "Accept": "*/*",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 "
                              "Safari/605.1.15",
                "referer": "https://www.google.com/"
            }

            url = "https://www.tesmanian.com/blogs/tesmanian-blog"
            req = requests.get(url, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, "lxml")

            page = soup.find_all(class_="eleven columns omega align_left")

            for item in page:
                id_url = item.find("a", class_="disqus-comment-count").get("data-disqus-identifier")

                if id_url in all_news:
                    time.sleep(15)
                    continue

                else:
                    item_text = item.find("h2").text
                    links = "https://www.tesmanian.com" + item.find('a').get('href')

                    all_news[id_url] = {
                        "title": item_text,
                        "link": links
                    }

                    send_telegram(f"{item_text}\n{links}")
                time.sleep(15)
                with open("news_dict.json", "a") as file:
                    json.dump(all_news, file, indent=4, ensure_ascii=False)


        except Exception as e:
            print(e)
            check_update_news()

def news_pars():

    try:

        url = "https://www.tesmanian.com/"
        pars_url = "blogs/tesmanian-blog"
        headers = {
            "Accept": "*/*",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 "
                          "Safari/605.1.15",
            "referer": "https://www.google.com/"
            }

        req = requests.get(url+pars_url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")

        page = soup.find_all(class_="eleven columns omega align_left")

        all_news = {}
        for item in page:
            item_text = item.find("h2").text
            links = "https://www.tesmanian.com" + item.find('a').get('href')
            id_url = item.find("a", class_="disqus-comment-count").get("data-disqus-identifier")

            all_news[id_url] = {
                "title": item_text,
                "link": links
            }

        with open("news_dict.json", "w") as file:
            json.dump(all_news, file, indent=4, ensure_ascii=False)

        with open("news_dict.json") as file:
            all_news = json.load(file)

        for k, v in sorted(all_news.items()):
            news = f"{v['title']}\n" \
                   f"{v['link']}"

            send_telegram(news)

        check_update_news()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    news_pars()