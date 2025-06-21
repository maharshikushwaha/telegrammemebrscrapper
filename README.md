# 📦 Telegram Group Member Scraper

A powerful asynchronous Python script that uses [Telethon](https://github.com/LonamiWebs/Telethon) to scrape members from one or multiple Telegram groups and export detailed user data to a CSV file.

## 🚀 Features

- ✅ Scrape members from multiple public groups
- ✅ Collect extended user details:
  - Username, ID, Access Hash
  - First Name, Last Name
  - Phone (if visible)
  - Last Seen Status (Online/Recently/Hidden/etc.)
  - Verified and Bot flags
  - Language code (if visible)
- ✅ Batch scraping to reduce rate-limiting risk
- ✅ Resume-safe CSV export with header check
- ✅ Asynchronous and scalable

---

## 📂 Output Format

The script generates a file named `members.csv` with the following columns:

| Field         | Description                          |
|---------------|--------------------------------------|
| Username      | Telegram @username                   |
| User ID       | Unique Telegram ID                   |
| Access Hash   | Required for contacting the user     |
| First Name    | Visible first name                   |
| Last Name     | Visible last name                    |
| Phone         | If public                            |
| Is Bot        | `True` if the user is a bot          |
| Is Verified   | `True` if Telegram has verified them |
| Lang Code     | Language (e.g., `en`, `ru`)          |
| Last Seen     | Online status or last seen window    |

---

## 🛠️ Requirements

- Python 3.7+
- Telethon

### Install dependencies

```bash
pip install telethon
