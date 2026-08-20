import trafilatura
from fetch_feeds import fetch_articles


def extract_full_text(url):
    """Download a page and pull out clean article text, or None if it fails."""
    downloaded = trafilatura.fetch_url(url)
    if downloaded is None:
        return None
    text = trafilatura.extract(downloaded)
    return text


def deduplicate(articles):
    """Remove articles with near-identical titles (simple lowercase match)."""
    seen_titles = set()
    unique = []
    for article in articles:
        key = article["title"].strip().lower()
        if key not in seen_titles:
            seen_titles.add(key)
            unique.append(article)
    return unique


def enrich_with_full_text(articles):
    """Add full article text to each article dict. Skips articles that fail to extract."""
    enriched = []

    for article in articles:
        print(f"Extracting: {article['title'][:60]}...")
        text = extract_full_text(article["link"])

        if text is None or len(text.strip()) < 200:
            print("  Skipped (couldn't extract enough text)")
            continue

        article["full_text"] = text
        enriched.append(article)

    return enriched


if __name__ == "__main__":
    raw_articles = fetch_articles()
    deduped = deduplicate(raw_articles)
    print(f"\nAfter dedup: {len(deduped)} articles")

    final_articles = enrich_with_full_text(deduped)
    print(f"\nSuccessfully extracted full text for {len(final_articles)} articles")

    if final_articles:
        sample = final_articles[0]
        print(f"\n--- Sample: {sample['title']} ---")
        print(sample["full_text"][:500])
        print("...")