import re
import os
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import links

url_to_fetch = links.links


class IT_JOB_FINDER:

    def __init__(self):
        load_dotenv()
        self.bot_token = os.getenv('BOT_TOKEN')
        self.chat_id = os.getenv('CHAT_ID')
        self.min_char = 40


    def fetch_job(self, url):
        all_jobs = []
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        # extract text
        soup = BeautifulSoup(response.text, "html.parser")
        messages = soup.select(".tgme_widget_message_wrap")

        messages = messages[-10:]

        for msg in messages:
            text_le = msg.select_one(".tgme_widget_message_text")
            post_link_el = msg.select_one("a.tgme_widget_message_date")

            if not text_le or not post_link_el:
                continue

            post = {
                "text": text_le.get_text("\n", strip=True),
                "post_url": post_link_el.get("href", "").strip(),
            }

            all_jobs.append(post)

        return all_jobs

    def extract_it_jobs(self, all_jobs:list):
        it_jobs = []
        if not all_jobs:
            return []
        MIN_CHARS = 40
        IT_TERMS = [
            r"\bict\b",
            r"\bit\s+(officer|support|technician|specialist|manager|administrator|engineer|intern)\b",
            r"\bsoftware\b",
            r"\bdeveloper\b",
            r"\bprogrammer\b",
            r"\b(software|network|system|systems|cloud|devops|data|security|qa)\s+engineer\b",
            r"\bfront[\s-]?end\b",
            r"\bback[\s-]?end\b",
            r"\bfull[\s-]?stack\b",
            r"\bweb\s+(developer|designer|development)\b",
            r"\bmobile\s+(developer|app|development)\b",
            r"\b(flutter|react|angular|vue|django|flask|fastapi|node\.?js|laravel|spring\s?boot)\b",
            r"\b(python|javascript|typescript|java|c#|php|golang|rust|kotlin|swift)\b",
            r"\b(devops|sysadmin|system\s+admin|network\s+admin|database\s+admin|dba)\b",
            r"\b(cyber\s?security|information\s+security|penetration\s+tester)\b",
            r"\b(data\s+analyst|data\s+scientist|machine\s+learning|ai\s+engineer)\b",
            r"\b(qa\s+tester|quality\s+assurance|ui/ux|ux/ui)\b",
            r"\bhelp\s?desk\b",
        ]

        IT_PATTERN = re.compile("|".join(IT_TERMS), re.IGNORECASE)

        for job in all_jobs:

            if len(job.get("text")) > self.min_char and IT_PATTERN.search(job.get("text")):
                it_jobs.append(job)

        return it_jobs

    def notify_telegram(self, all_it_jobs: list):
       
        if not self.bot_token or not self.chat_id:
            raise ValueError("Missing BOT_TOKEN or CHAT_ID in .env file")
        
        api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        for it_job in all_it_jobs:

            post_text = it_job.get("text", "")[:3850]
            post_url = it_job.get("post_url")
            payload = {
                "chat_id": self.chat_id,
                "text": f"{post_text} \n\n\n ORIGINAL LINK: {post_url}"
            }
            response = requests.post(api_url, payload, timeout=15)
            response.raise_for_status()
            time.sleep(0.4)


    def exec(self, urls: list):
        all_channel_it_jobs = []

        for url in urls:
            all_jobs = self.fetch_job(url)
            it_jobs = self.extract_it_jobs(all_jobs)
            all_channel_it_jobs += it_jobs

        self.notify_telegram(all_channel_it_jobs)





test = IT_JOB_FINDER()

test.exec(['https://t.me/s/josad_it', 'https://t.me/s/geezjobs_ethiopia'])

