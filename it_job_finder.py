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

    def extract_it_jobs(self):
        if not self.all_jobs:
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

        for job in self.all_jobs:

            if len(job.get("text")) > MIN_CHARS and IT_PATTERN.search(job.get("text")):
                self.it_jobs.append(job)


test = IT_JOB_FINDER()
test.fetch_job(url="https://t.me./s/josad_it")

test.extract_it_jobs()

print(test.it_jobs)
