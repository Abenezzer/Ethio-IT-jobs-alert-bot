import re
import os
import time
import sqlite3
from datetime import datetime, timedelta, timezone
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import links

class IT_JOB_FINDER:

    def __init__(
        self, db_path: str = "jobs.db", min_char: int = 40, retention_days: int = 30
    ):

        load_dotenv()
        self.bot_token = os.getenv("BOT_TOKEN")
        self.channel_id = os.getenv("CHANNEL_ID")
        self.min_char = min_char
    
        self.db_path = db_path
        self.retention_days = retention_days

        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._get_conn() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS seen_jobs(
                post_url TEXT PRIMARY KEY,
                seen_at TEXT NOT NULL
            )
            """)
            conn.commit()

    def cleanup_old_jobs(self) -> int:
        """Delete entires older than `self.retention_days`"""

        cutoff = (
            datetime.now(timezone.utc) - timedelta(days=self.retention_days)
        ).isoformat()

        with self._get_conn() as conn:
            cursor = conn.execute(
                "DELETE FROM seen_jobs WHERE seen_at < ?",
                (cutoff,),
            )
            conn.commit()
            return cursor.rowcount

    def is_seen(self, post_url) -> bool:
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT 1 FROM seen_jobs WHERE post_url = ? LIMIT 1",
                (post_url,),
            ).fetchone()
            return row is not None

    def mark_seen(self, post_url) -> None:
        with self._get_conn() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO seen_jobs(post_url, seen_at) VALUES(?, ?)",
                (post_url, datetime.now(timezone.utc).isoformat()),
            )
            conn.commit()

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

    def extract_it_jobs(self, all_jobs: list):
        it_jobs = []
        if not all_jobs:
            return []
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
            if len(job.get("text")) > self.min_char and IT_PATTERN.search(
                job.get("text")
            ):
                it_jobs.append(job)

        return it_jobs

    def notify_telegram(self, all_it_jobs: list):

        if not self.bot_token or not self.channel_id:
            raise ValueError("Missing BOT_TOKEN or CHANNEL_ID in .env file")

        api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        for it_job in all_it_jobs:
            if not self.is_seen(it_job.get("post_url")):
                post_text = it_job.get("text", "")[:3850]
                post_url = it_job.get("post_url")
                payload = {
                    "chat_id": self.channel_id,
                    "text": f"{post_text} \n\n\n ORIGINAL LINK: {post_url}",
                }
                response = requests.post(api_url, payload, timeout=15)
                response.raise_for_status()
                time.sleep(0.4)
               
                self.mark_seen(it_job.get("post_url"))

    def exec(self, urls: list):

        self.cleanup_old_jobs()

        all_channel_it_jobs = []
        for url in urls:
            all_jobs = self.fetch_job(url)
            it_jobs = self.extract_it_jobs(all_jobs)
            all_channel_it_jobs += it_jobs

        self.notify_telegram(all_channel_it_jobs)



if __name__ == "__main__":
    urls_to_fetch = links.urls
    try:
        finder = IT_JOB_FINDER()
        finder.exec(urls_to_fetch)
    except Exception as e:
        print(e)
