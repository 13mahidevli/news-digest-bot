from datetime import date
from collections import defaultdict

from summarize import fetch_articles, deduplicate, enrich_with_full_text, summarize_all


def group_by_topic(articles):
    """Group a flat list of articles into a dict keyed by topic."""
    grouped = defaultdict(list)
    for article in articles:
        grouped[article["topic"]].append(article)
    return grouped


def build_html_digest(articles):
    """Turn a list of summarized articles into a full HTML email string."""
    grouped = group_by_topic(articles)
    today = date.today().strftime("%B %d, %Y")

    html_parts = [f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #222;">
        <h1 style="font-size: 22px; border-bottom: 2px solid #333; padding-bottom: 8px;">
            Your Daily Digest — {today}
        </h1>
    """]

    for topic, topic_articles in grouped.items():
        html_parts.append(f'<h2 style="font-size: 18px; margin-top: 28px; color: #444;">{topic}</h2>')

        for article in topic_articles:
            html_parts.append(f"""
            <div style="margin-bottom: 18px;">
                <a href="{article['link']}" style="font-size: 16px; font-weight: bold; color: #1a0dab; text-decoration: none;">
                    {article['title']}
                </a>
                <p style="font-size: 14px; line-height: 1.5; color: #333; margin: 6px 0 0 0;">
                    {article['summary']}
                </p>
            </div>
            """)

    html_parts.append("</body></html>")
    return "".join(html_parts)


if __name__ == "__main__":
    raw_articles = fetch_articles()
    deduped = deduplicate(raw_articles)
    extracted = enrich_with_full_text(deduped)

    print(f"\nSummarizing {len(extracted)} articles with Gemini...\n")
    summarized = summarize_all(extracted)

    html = build_html_digest(summarized)

    with open("digest_preview.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("\nDigest saved to digest_preview.html — open it in your browser to preview.")