# Ethio IT Jobs Alert Bot

An automated, zero-cost IT job aggregator for Ethiopia that scrapes recent posts from public Telegram job channels, filters for IT and software-related roles using regular expressions, deduplicates listings with SQLite, and broadcasts matching opportunities to a public Telegram channel (**`@ethio_it_jobs`**) on a daily schedule via GitHub Actions.

---

## Overview

Job seekers in Ethiopia often have to check multiple Telegram channels every day to avoid missing tech openings—while wading through roles outside IT. **Ethio IT Jobs Alert Bot** centralizes discovery by pulling recent posts from popular Ethiopian Telegram job sources, filtering for IT keywords, tracking previously posted URLs so subscribers don't see duplicates, and publishing clean alerts with a link back to the original post.

---

## Key Features

* **Centralized Ethiopian Job Aggregation:** Pulls recent posts from configured public Telegram channel web previews (`https://t.me/s/...`) defined in `links.py`.
* **Targeted IT Keyword Filtering:** Uses case-insensitive regular expressions (`IT_PATTERN`) and a minimum character threshold (`min_char`) to isolate IT, software engineering, data, networking, security, QA, and support roles.
* **Duplicate Prevention (`sqlite3`):** Stores seen `post_url` entries and UTC timestamps (`seen_at`) in `jobs.db` (`seen_jobs` table), plus tracks URLs already dispatched within the current run.
* **Automated Database Retention:** `cleanup_old_jobs()` prunes records older than `retention_days` (default: `30` days) to keep `jobs.db` tidy.
* **Telegram Channel Broadcasting:** Sends formatted alerts to `@ethio_it_jobs` via the Telegram Bot API (`/sendMessage`), including the original post link and safe message length truncation.
* **Zero-Cost Daily Automation:** Runs automatically every day at **07:00 AM EAT (`04:00` UTC)** using GitHub Actions (`cron: "0 4 * * *"`) and commits updated `jobs.db` state back to the repository.

---

## Tech Stack

* **Language:** Python 3
* **HTTP & Scraping:** `requests`, `BeautifulSoup4`
* **Filtering:** Python `re` (regular expressions)
* **Persistence:** `sqlite3` (`jobs.db`)
* **Environment & Dependencies:** `python-dotenv`, `pipenv` (`Pipfile` & `Pipfile.lock`)
* **Delivery & Automation:** Telegram Bot API, GitHub Actions

---

## Project Structure

```text
Ethio-IT-jobs-alert-bot/
├── .github/
│   └── workflows/
│       └── daily_jobs.yml     # Scheduled (cron) & manual GitHub Actions workflow
├── it_job_finder.py           # IT_JOB_FINDER class: scrape, filter, deduplicate, notify
├── links.py                   # List of target Telegram preview URLs ([https://t.me/s/](https://t.me/s/)...)
├── jobs.db                    # SQLite database storing seen job URLs and timestamps
├── Pipfile                    # Project dependencies managed by Pipenv
├── Pipfile.lock               # Locked dependency versions for reproducible installs
├── .env                       # Local secrets (ignored by Git)
└── README.md
