import os
import time
from dotenv import load_dotenv
from google import genai

from extract_articles import fetch_articles, deduplicate, enrich_with_full_text

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

client = genai.Client(api_key=api_key)
MODEL_NAME = "gemini-3.5-flash-lite"

SUMMARY_PROMPT = """Summarize the following news article in 2-3 concise sentences for a daily news digest email. Be neutral and factual. Do not include a headline, just the summary text.

Article:
{article_text}
"""


def summarize_article(article_text):
    """Send article text to Gemini and return a short summary string."""
    prompt = SUMMARY_PROMPT.format(article_text=article_text[:6000])  # cap length to stay well within limits
    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return response.text.strip()


def summarize_all(articles):
    """Add a 'summary' field to each article dict."""
    summarized = []

    for article in articles:
        print(f"Summarizing: {article['title'][:60]}...")
        try:
            summary = summarize_article(article["full_text"])
            article["summary"] = summary
            summarized.append(article)
        except Exception as e:
            print(f"  Failed to summarize: {e}")

        time.sleep(1)  # small delay to stay well under free-tier rate limits

    return summarized


if __name__ == "__main__":
    raw_articles = fetch_articles()
    deduped = deduplicate(raw_articles)
    extracted = enrich_with_full_text(deduped)

    print(f"\nSummarizing {len(extracted)} articles with Gemini...\n")
    final_articles = summarize_all(extracted)

    print(f"\nDone. Summarized {len(final_articles)} articles.\n")

    for article in final_articles:
        print(f"[{article['topic']}] {article['title']}")
        print(f"  {article['summary']}\n")