import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

from format_digest import (
    fetch_articles, deduplicate, enrich_with_full_text,
    summarize_all, build_html_digest
)

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
    raise ValueError("EMAIL_ADDRESS or EMAIL_APP_PASSWORD not found. Check your .env file.")

# Who receives the digest — for now, send it to yourself
RECIPIENT_EMAIL = EMAIL_ADDRESS


def send_email(subject, html_body, to_email):
    """Send an HTML email via Gmail SMTP."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.send_message(msg)


if __name__ == "__main__":
    raw_articles = fetch_articles()
    deduped = deduplicate(raw_articles)
    extracted = enrich_with_full_text(deduped)

    print(f"\nSummarizing {len(extracted)} articles with Gemini...\n")
    summarized = summarize_all(extracted)

    html = build_html_digest(summarized)

    print(f"\nSending digest to {RECIPIENT_EMAIL}...")
    send_email(
        subject="Your Daily News Digest",
        html_body=html,
        to_email=RECIPIENT_EMAIL,
    )
    print("Email sent successfully!")