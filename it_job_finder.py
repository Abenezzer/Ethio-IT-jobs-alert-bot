import re
import requests
from bs4 import BeautifulSoup
import links

url_to_fetch = links.links


class IT_JOB_FINDER:

    def __init__(self):
        self.all_jobs = []
        self.it_jobs = []

    def fetch_job(self, url):
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        # extract text
        soup = BeautifulSoup(response.text, "html.parser")
        messages = soup.select(".tgme_widget_message_wrap")

        for msg in messages:
            text_le = msg.select_one(".tgme_widget_message_text")
            post_link_el = msg.select_one("a.tgme_widget_message_date")

            if not text_le or not post_link_el:
                continue

            post = {
                "text": text_le.get_text("\n", strip=True),
                "post_url": post_link_el.get("href", "").strip(),
            }

            self.all_jobs.append(post)


test = IT_JOB_FINDER()
test.fetch_job(url =  'https://t.me./s/josad_it')

print(test.all_jobs)