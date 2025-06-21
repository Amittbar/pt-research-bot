
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

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GMAIL_ADDRESS = "amittbar@gmail.com"
GMAIL_APP_PASSWORD = "kmlrtwbcoiuwznqz"
RECEIVER_EMAIL = "amittbar@gmail.com"

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
            papers = response.json().get("abstracts", [])
        except Exception as e:
            print(f"[❌] Failed to decode ScholarAI JSON: {e}")
            return None, None

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

# Remaining functions unchanged from earlier script
