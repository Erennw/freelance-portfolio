import requests
from bs4 import BeautifulSoup
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ─── Bot Configuration ───
BOT_TOKEN = "8727309809:AAGoXDtUBx7iwbHmEJ4s3W_HNQBFxkyRH0k"


# ─── /start Command ───
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = (
        "👋 Welcome! I'm your News & Utility Bot.\n\n"
        "Here are the available commands:\n\n"
        "🕐 /time - Show current date and time\n"
        "📰 /scrape - Fetch the latest 5 news from BBC\n"
        "❓ /help - Show this message again"
    )
    await update.message.reply_text(welcome)


# ─── /help Command ───
async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_start(update, context)


# ─── /time Command ───
async def cmd_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now()
    text = (
        f"📅 Date: {now.strftime('%d %B %Y')}\n"
        f"🕐 Time: {now.strftime('%H:%M:%S')}\n"
        f"📆 Day: {now.strftime('%A')}"
    )
    await update.message.reply_text(text)


# ─── /scrape Command ───
async def cmd_scrape(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Fetching latest news from BBC...")

    try:
        articles = scrape_bbc(limit=5)

        if not articles:
            await update.message.reply_text("❌ No articles found. BBC may have changed its page structure.")
            return

        response = "📰 *Latest BBC News*\n" + "─" * 25 + "\n\n"

        for i, article in enumerate(articles, 1):
            title = article["title"].replace("*", "").replace("_", "")
            date_str = f"📅 {article['date']}" if article["date"] else ""
            response += f"*{i}.* {title}\n🔗 [Read more]({article['link']})\n{date_str}\n\n"

        await update.message.reply_text(response, parse_mode="Markdown", disable_web_page_preview=True)

    except Exception as e:
        await update.message.reply_text(f"❌ Error while scraping: {str(e)}")


def scrape_bbc(limit=5):
    """Fetch latest news articles from BBC News (from Project 1)."""
    url = "https://www.bbc.com/news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    seen = set()

    for a_tag in soup.find_all("a", href=True):
        if len(articles) >= limit:
            break

        href = a_tag["href"]

        # Filter only news article URLs
        if "/news/articles/" not in href and "/news/videos/" not in href:
            continue

        # Build full URL
        if href.startswith("/"):
            href = "https://www.bbc.com" + href

        # Find headline text
        title = ""
        h_tag = a_tag.find(["h1", "h2", "h3", "h4", "h5", "h6"])
        if h_tag:
            title = h_tag.get_text(strip=True)
        else:
            span = a_tag.find("span") or a_tag.find("p")
            if span:
                title = span.get_text(strip=True)
            else:
                title = a_tag.get_text(strip=True)

        if not title or len(title) < 10:
            continue

        # Skip duplicates
        if title in seen:
            continue
        seen.add(title)

        # Search for date in parent elements
        date = ""
        parent = a_tag.parent
        for _ in range(5):
            if parent is None:
                break
            time_tag = parent.find("time")
            if time_tag:
                date = time_tag.get_text(strip=True) or time_tag.get("datetime", "")
                break
            parent = parent.parent

        articles.append({"title": title, "link": href, "date": date})

    return articles


# ─── Start Bot ───
if __name__ == "__main__":
    print("🤖 Bot is running... Press Ctrl+C to stop.")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("time", cmd_time))
    app.add_handler(CommandHandler("scrape", cmd_scrape))

    app.run_polling()