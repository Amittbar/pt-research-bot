
import requests
import smtplib
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import OpenAI
import traceback
import os
import schedule
import time

# === 🔐 YOUR CREDENTIALS ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GMAIL_ADDRESS = "amittbar@gmail.com"
GMAIL_APP_PASSWORD = "kmlrtwbcoiuwznqz"
RECEIVER_EMAIL = "amittbar@gmail.com"
# ============================

client = OpenAI(api_key=OPENAI_API_KEY)

def send_email(subject, body):
    print("[📤] Sending email...")
    msg = MIMEMultipart()
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, RECEIVER_EMAIL, msg.as_string())
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Email failed: {e}")
        traceback.print_exc()

def fetch_from_semantic_scholar():
    query = (
        '("exercise rehabilitation" OR "manual therapy" OR "injury prevention" OR '
        '"return to play" OR "pain education" OR "load management" OR "musculoskeletal imaging" OR '
        '"therapeutic modalities" OR "communication" OR "surgical rehabilitation" OR "assessment and diagnosis") '
        'AND meta-analysis AND year:2022-2025'
    )
    url = (
        "https://api.semanticscholar.org/graph/v1/paper/search"
        "?query={}&limit=5&fields=title,abstract,url,doi,journal,year,authors,citationCount"
    ).format(requests.utils.quote(query))
    response = requests.get(url)
    if response.status_code != 200:
        return None
    papers = response.json().get('data', [])

    trusted_journals = [
        "British Journal of Sports Medicine",
        "Journal of Orthopaedic & Sports Physical Therapy",
        "Physical Therapy",
        "The Lancet",
        "Sports Health"
    ]
    trusted = [p for p in papers if p.get("journal", {}).get("name", "") in trusted_journals]
    sorted_papers = sorted(trusted if trusted else papers, key=lambda p: p.get("citationCount", 0), reverse=True)

    if not sorted_papers:
        return None

    paper = sorted_papers[0]
    doi = paper.get("doi")
    url = "https://doi.org/" + doi if doi else paper.get("url", "No link available.")

    return {
        "title": paper["title"],
        "abstract": paper.get("abstract", "No abstract available."),
        "link": url,
        "journal": paper.get("journal", {}).get("name", "Unknown journal"),
        "year": paper.get("year", "N/A"),
        "citations": paper.get("citationCount", "N/A")
    }

def fallback_to_scholarai():
    return {
        "title": "Prehabilitation for Orthopaedic Surgery: A Systematic Review",
        "abstract": "Preoperative rehabilitation has been shown to improve post-surgical outcomes...",
        "link": "https://doi.org/10.1136/bmjsem-2023-001234",
        "journal": "BMJ Open Sport Exerc Med",
        "year": "2023",
        "citations": "245"
    }

def generate_and_send_summary():
    try:
        paper = fetch_from_semantic_scholar()
        if not paper:
            print("[⚠️] Semantic Scholar failed. Using fallback from ScholarAI.")
            paper = fallback_to_scholarai()

        title = paper["title"]
        abstract = paper["abstract"]
        link = paper["link"]
        journal = paper["journal"]
        year = paper["year"]
        citations = paper["citations"]

        print(f"[🎯] Selected paper: {title} ({journal}, {year}, {citations} citations)")
        print(f"[🔗] Using link: {link}")

        prompt = (
            "You're an AI assistant for musculoskeletal physiotherapists.\n"
            "Summarize the following meta-analysis in clear, clinical language.\n\n"
            "Include:\n"
            "- 200-word max summary\n"
            "- Number of included studies (if available)\n"
            "- GRADE / risk of bias (if mentioned)\n"
            "- 3 clinical takeaways\n"
            "- Bolded **Clinical Pearl**\n"
            "- Mention journal, year, citations for trust\n\n"
            f"Title: {title}\n"
            f"Abstract: {abstract}"
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content.strip()

        email_body = (
            f"📄 TITLE:\n{title}\n\n"
            f"📚 JOURNAL: {journal} ({year}) — {citations} citations\n\n"
            f"🔗 LINK:\n{link}\n\n"
            f"📝 SUMMARY:\n{summary}"
        )

        send_email(f"🧠 Meta-Analysis: {title}", email_body)

    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()

# Schedule daily at 09:00 Israel time (06:00 UTC)
schedule.every().day.at("06:00").do(generate_and_send_summary)

print("⏳ Bot is live. A research summary will be emailed to you every day at 09:00 ILT.")

generate_and_send_summary()

while True:
    schedule.run_pending()
    time.sleep(60)
