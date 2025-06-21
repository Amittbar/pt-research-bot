
import requests
import smtplib
import random
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
    print("[📤] Preparing to send email...")
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

def fetch_scholarai_paper():
    try:
        print("[📥] Fetching paper from ScholarAI...")
        url = "https://api.scholarai.io/api/searchAbstracts"
        payload = {
            "full_user_prompt": "search for meta-analyses related to physical therapy including exercise rehabilitation, manual therapy, surgical rehab, pain science, or return to play.",
            "keywords": "physical therapy, meta-analysis, musculoskeletal rehabilitation, surgical rehab, pain science, return to play",
            "sort": "publication_date",
            "query": "meta-analysis AND (physical therapy OR exercise rehabilitation OR surgical rehab OR pain science OR return to play)",
            "generative_mode": "true"
        }
                response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"[❌] ScholarAI API error: {response.status_code}")
            return None, None
        try:
            # handled above with try/except
        except Exception as e:
            print(f"[❌] Failed to decode ScholarAI JSON: {e}")
            return None, None
        # handled above with try/except
        if not papers:
            return None, None

        paper = papers[0]
        return {
            "title": paper["title"],
            "abstract": paper["abstract"],
            "pmid": paper.get("doi", "N/A"),
            "journal": paper.get("journal", "ScholarAI Source"),
            "year": paper.get("publicationDate", "N/A")[:4],
            "citations": paper.get("cited_by_count", "N/A"),
            "source": "[ScholarAI]"
        }, paper["landing_page_url"]
    except Exception as e:
        print(f"[⚠️] ScholarAI fetch failed: {e}")
        traceback.print_exc()
        return None, None

def fetch_from_semantic_scholar():
    try:
        print("[📥] Trying fallback: Semantic Scholar...")
        query = (
            '("exercise rehabilitation" OR "manual therapy" OR "injury prevention" OR '
            '"return to play" OR "pain education" OR "load management" OR "musculoskeletal imaging" OR '
            '"therapeutic modalities" OR "communication" OR "surgical rehabilitation" OR "assessment and diagnosis") '
            'AND meta-analysis AND year:2022-2025'
        )
        url = (
            "https://api.semanticscholar.org/graph/v1/paper/search"
            "?query={}&limit=20&fields=title,abstract,url,doi,journal,year,authors,citationCount"
        ).format(requests.utils.quote(query))
        papers = []
        for offset in range(0, 60, 20):
            paginated_url = url + f"&offset={offset}"
            response = requests.get(paginated_url)
            if response.status_code == 200:
                batch = response.json().get("data", [])
                papers.extend(batch)

        valid_papers = [p for p in papers if p.get("abstract") and p.get("title")]
        if not valid_papers:
            return None, None

        selected = random.choice(valid_papers)
        return {
            "title": selected["title"],
            "abstract": selected.get("abstract", "No abstract available."),
            "pmid": selected.get("doi", "N/A"),
            "journal": selected.get("journal", {}).get("name", "Unknown journal"),
            "year": selected.get("year", "N/A"),
            "citations": selected.get("citationCount", "N/A"),
            "source": "[Semantic Scholar]"
        }, selected.get("url", "No URL")
    except Exception as e:
        print(f"[⚠️] Semantic Scholar fetch failed: {e}")
        traceback.print_exc()
        return None, None

def generate_and_send_summary():
    print("[⏳] Starting daily summary generation...")
    try:
        paper, url = fetch_scholarai_paper()
        if not paper:
            print("[🔁] ScholarAI failed, trying Semantic Scholar.")
            paper, url = fetch_from_semantic_scholar()
        if not paper:
            print("[❌] No paper available from any source.")
            return

        title = paper["title"]
        abstract = paper["abstract"]
        pmid = paper["pmid"]
        journal = paper["journal"]
        year = paper["year"]
        citations = paper["citations"]
        source = paper["source"]

        print(f"[📄] {title} | {journal} ({year}) | Citations: {citations} | PMID: {pmid} | Source: {source}")

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

        print("[🧠] Generating GPT summary...")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content.strip()

        email_body = (
            f"📄 TITLE:\n{title}\n\n"
            f"📚 JOURNAL: {journal} ({year}) — {citations} citations\n\n"
            f"🆔 PMID / DOI: {pmid}\n\n"
            f"📡 SOURCE: {source}\n\n"
            f"📝 SUMMARY:\n{summary}"
        )

        print(f"[📤] Sending email to {RECEIVER_EMAIL}...")
        send_email(f"🧠 Meta-Analysis: {title}", email_body)
        print("[✅] Summary email sent successfully!")

    except Exception as e:
        print(f"[❌] Summary process failed: {e}")
        traceback.print_exc()

schedule.every().day.at("06:00").do(generate_and_send_summary)
generate_and_send_summary()

print("[🚀] Bot is live and scheduled.")
while True:
    schedule.run_pending()
    time.sleep(60)
