import requests
import smtplib
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import OpenAI
import schedule
import time

# === 🔐 YOUR CREDENTIALS ===
import requests
import smtplib
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import OpenAI
import schedule
import time

# === 🔐 YOUR CREDENTIALS ===
import requests
import smtplib
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import OpenAI
import schedule
import time

# === 🔐 YOUR CREDENTIALS ===
import os
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

def generate_and_send_summary():
    try:
        # Step 1: Query Semantic Scholar
        query = (
            '("musculoskeletal injury" OR "physical therapy") '
            'AND meta-analysis AND year:2022-2025'
        )
        url = (
            "https://api.semanticscholar.org/graph/v1/paper/search"
            f"?query={query}&limit=5&fields=title,abstract,url,journal,year,authors,citationCount"
        )
        response = requests.get(url)
        papers = response.json().get('data', [])

        # Step 2: Filter by journal
        trusted_journals = [
            "British Journal of Sports Medicine",
            "Journal of Orthopaedic & Sports Physical Therapy",
            "Physical Therapy",
            "The Lancet",
            "Sports Health"
        ]

        sorted_papers = sorted(
            [p for p in papers if p.get("journal", {}).get("name", "") in trusted_journals],
            key=lambda p: p.get("citationCount", 0),
            reverse=True
        )

        if not sorted_papers:
            raise Exception("No high-trust meta-analyses found.")

        top_paper = sorted_papers[0]
        title = top_paper["title"]
        abstract = top_paper.get("abstract", "No abstract available.")
        link = top_paper.get("url", "No link available.")
        journal = top_paper.get("journal", {}).get("name", "Unknown journal")
        year = top_paper.get("year", "N/A")
        citations = top_paper.get("citationCount", "N/A")

        print(f"[🎯] Selected paper: {title} ({journal}, {year}, {citations} citations)")

        # Step 3: GPT summary
        prompt = f"""
You're an AI assistant for musculoskeletal physiotherapists.
Summarize the following meta-analysis in clear, clinical language.

Include:
- 200-word max summary
- Number of included studies (if available)
- GRADE / risk of bias (if mentioned)
- 3 clinical takeaways
- Bolded **Clinical Pearl**
- Mention journal, year, citations for trust

Title: {title}
Abstract: {abstract}
"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt.strip()}]
        )
        summary = response.choices[0].message.content.strip()

        # Step 4: Email formatting
        email_body = (
            f"EVIDENCE-AWARE PT DIGEST\n\n"
            f"📄 TITLE:\n{title}\n\n"
            f"📚 JOURNAL: {journal} ({year}) — {citations} citations\n\n"
            f"🔗 LINK:\n{link}\n\n"
            f"📝 SUMMARY:\n{summary}\n\n"
            f"---\nThis summary is based on a peer-reviewed meta-analysis from a trusted journal."
        )

        send_email(f"🧠 Meta-Analysis: {title}", email_body)

    except Exception as e:
        print(f"❌ Error: {e}")

# Schedule daily at 09:00 Israel time (06:00 UTC)
schedule.every().day.at("06:00").do(generate_and_send_summary)

print("⏳ Bot is live. A research summary will be emailed to you every day at 09:00 ILT.")

while True:
    schedule.run_pending()
    time.sleep(60)  
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

def generate_and_send_summary():
    try:
        # Step 1: Query Semantic Scholar
        query = (
            '("musculoskeletal injury" OR "physical therapy") '
            'AND meta-analysis AND year:2022-2025'
        )
        url = (
            "https://api.semanticscholar.org/graph/v1/paper/search"
            f"?query={query}&limit=5&fields=title,abstract,url,journal,year,authors,citationCount"
        )
        response = requests.get(url)
        papers = response.json().get('data', [])

        # Step 2: Filter by journal
        trusted_journals = [
            "British Journal of Sports Medicine",
            "Journal of Orthopaedic & Sports Physical Therapy",
            "Physical Therapy",
            "The Lancet",
            "Sports Health"
        ]

        sorted_papers = sorted(
            [p for p in papers if p.get("journal", {}).get("name", "") in trusted_journals],
            key=lambda p: p.get("citationCount", 0),
            reverse=True
        )

        if not sorted_papers:
            raise Exception("No high-trust meta-analyses found.")

        top_paper = sorted_papers[0]
        title = top_paper["title"]
        abstract = top_paper.get("abstract", "No abstract available.")
        link = top_paper.get("url", "No link available.")
        journal = top_paper.get("journal", {}).get("name", "Unknown journal")
        year = top_paper.get("year", "N/A")
        citations = top_paper.get("citationCount", "N/A")

        print(f"[🎯] Selected paper: {title} ({journal}, {year}, {citations} citations)")

        # Step 3: GPT summary
        prompt = f"""
You're an AI assistant for musculoskeletal physiotherapists.
Summarize the following meta-analysis in clear, clinical language.

Include:
- 200-word max summary
- Number of included studies (if available)
- GRADE / risk of bias (if mentioned)
- 3 clinical takeaways
- Bolded **Clinical Pearl**
- Mention journal, year, citations for trust

Title: {title}
Abstract: {abstract}
"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt.strip()}]
        )
        summary = response.choices[0].message.content.strip()

        # Step 4: Email formatting
        email_body = (
            f"EVIDENCE-AWARE PT DIGEST\n\n"
            f"📄 TITLE:\n{title}\n\n"
            f"📚 JOURNAL: {journal} ({year}) — {citations} citations\n\n"
            f"🔗 LINK:\n{link}\n\n"
            f"📝 SUMMARY:\n{summary}\n\n"
            f"---\nThis summary is based on a peer-reviewed meta-analysis from a trusted journal."
        )

        send_email(f"🧠 Meta-Analysis: {title}", email_body)

    except Exception as e:
        print(f"❌ Error: {e}")

# Schedule daily at 09:00 Israel time (06:00 UTC)
schedule.every().day.at("06:00").do(generate_and_send_summary)

print("⏳ Bot is live. A research summary will be emailed to you every day at 09:00 ILT.")

while True:
    schedule.run_pending()
    time.sleep(60)  
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

def generate_and_send_summary():
    try:
        # Step 1: Query Semantic Scholar
        query = (
            '("musculoskeletal injury" OR "physical therapy") '
            'AND meta-analysis AND year:2022-2025'
        )
        url = (
            "https://api.semanticscholar.org/graph/v1/paper/search"
            f"?query={query}&limit=5&fields=title,abstract,url,journal,year,authors,citationCount"
        )
        response = requests.get(url)
        papers = response.json().get('data', [])

        # Step 2: Filter by journal
        trusted_journals = [
            "British Journal of Sports Medicine",
            "Journal of Orthopaedic & Sports Physical Therapy",
            "Physical Therapy",
            "The Lancet",
            "Sports Health"
        ]

        sorted_papers = sorted(
            [p for p in papers if p.get("journal", {}).get("name", "") in trusted_journals],
            key=lambda p: p.get("citationCount", 0),
            reverse=True
        )

        if not sorted_papers:
            raise Exception("No high-trust meta-analyses found.")

        top_paper = sorted_papers[0]
        title = top_paper["title"]
        abstract = top_paper.get("abstract", "No abstract available.")
        link = top_paper.get("url", "No link available.")
        journal = top_paper.get("journal", {}).get("name", "Unknown journal")
        year = top_paper.get("year", "N/A")
        citations = top_paper.get("citationCount", "N/A")

        print(f"[🎯] Selected paper: {title} ({journal}, {year}, {citations} citations)")

        # Step 3: GPT summary
        prompt = f"""
You're an AI assistant for musculoskeletal physiotherapists.
Summarize the following meta-analysis in clear, clinical language.

Include:
- 200-word max summary
- Number of included studies (if available)
- GRADE / risk of bias (if mentioned)
- 3 clinical takeaways
- Bolded **Clinical Pearl**
- Mention journal, year, citations for trust

Title: {title}
Abstract: {abstract}
"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt.strip()}]
        )
        summary = response.choices[0].message.content.strip()

        # Step 4: Email formatting
        email_body = (
            f"EVIDENCE-AWARE PT DIGEST\n\n"
            f"📄 TITLE:\n{title}\n\n"
            f"📚 JOURNAL: {journal} ({year}) — {citations} citations\n\n"
            f"🔗 LINK:\n{link}\n\n"
            f"📝 SUMMARY:\n{summary}\n\n"
            f"---\nThis summary is based on a peer-reviewed meta-analysis from a trusted journal."
        )

        send_email(f"🧠 Meta-Analysis: {title}", email_body)

    except Exception as e:
        print(f"❌ Error: {e}")

# Schedule daily at 09:00 Israel time (06:00 UTC)
schedule.every().day.at("06:00").do(generate_and_send_summary)

print("⏳ Bot is live. A research summary will be emailed to you every day at 09:00 ILT.")

while True:
    schedule.run_pending()
    time.sleep(60)
