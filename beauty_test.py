import requests
from bs4 import BeautifulSoup


url  = 'https://t.me./s/ethiojobsofficialclear'

response = requests.get(url=url, timeout=15)

soup = BeautifulSoup(response.text, "html.parser")

messages = soup.select(".tgme_widget_message_wrap")


for message in messages:
    text_el = message.select_one('.tgme_widget_message_text')
    text = text_el.get_text('\n', strip=True)[:300]
    post_link_el = message.select_one("a.tgme_widget_message_date")
    post_url = post_url = post_link_el["href"] if post_link_el and post_link_el.get("href") else ""

    payload = f"""
               --POST--- \n
               Review: {text} \n\n
               Post URL: {post_url},
            """

    print(payload)


   