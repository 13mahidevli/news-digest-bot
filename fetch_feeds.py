import feedparser

# Add or remove feeds here based on the topics you care about
FEEDS = {
    "Tech": "https://www.theverge.com/rss/index.xml",
    "World News": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "Business": "https://feeds.bbci.co.uk/news/business/rss.xml",
}


def fetch_articles():
    """Fetch the latest articles from each configured RSS feed."""
    all_articles = []

    for topic, url in FEEDS.items():
        print(f"\nFetching: {topic}")
        feed = feedparser.parse(url)

        if feed.bozo:
            print(f"  Warning: couldn't parse feed cleanly ({feed.bozo_exception})")

        for entry in feed.entries[:5]:  # just the 5 most recent per feed for now
            article = {
                "topic": topic,
                "title": entry.get("title", "No title"),
                "link": entry.get("link", ""),
                "published": entry.get("published", "Unknown date"),
            }
            all_articles.append(article)
            print(f"  - {article['title']}")

    return all_articles


if __name__ == "__main__":
    articles = fetch_articles()
    print(f"\nTotal articles fetched: {len(articles)}")