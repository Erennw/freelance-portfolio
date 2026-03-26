# Telegram Bot

A Telegram bot that can announce the date and time and scrape the first five news articles from the first project

## Features
- There are four commands available: /start displays a welcome message and the list of commands, /help displays the same message again, /time displays the current date and time, and /scrape fetches the latest 5 BBC news stories.
- /scrape sends the latest 5 news stories from BBC News as a single Telegram message.
- The bot runs continuously and in real time because it is waiting for a command

## Technologies
- Python
- python-telegram-bot
- Requests
- BeautifulSoup4

## Usage
```bash
pip install python-telegram-bot requests beautifulsoup4

Replace the “Add token” section in the file with the token you received from BotFather, then:

python telegram_bot.py
```