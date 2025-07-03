# crawler_and_extractor.py

import os
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF

# --- Config ---
BASE_URL = "https://www.mosdac.gov.in"
TARGET_URL = "https://www.mosdac.gov.in/data/"
PDF_FOLDER = "downloaded_pdfs"
os.makedirs(PDF_FOLDER, exist_ok=True)

# --- Step 1: Crawl for PDFs ---
response = requests.get(TARGET_URL)
soup = BeautifulSoup(response.content, "html.parser")

pdf_links = []
for link in soup.find_all("a"):
    href = link.get("href")
    if href and ".pdf" in href:
        full_url = BASE_URL + href
        pdf_links.append(full_url)

print(f"🔍 Found {len(pdf_links)} PDFs")

# --- Step 2: Download PDFs ---
downloaded = []
for url in pdf_links:
    filename = os.path.join(PDF_FOLDER, url.split("/")[-1])
    if not os.path.exists(filename):
        try:
            r = requests.get(url)
            with open(filename, "wb") as f:
                f.write(r.content)
            downloaded.append(filename)
            print(f"⬇️  Downloaded: {filename}")
        except Exception as e:
            print(f"❌ Failed to download {url}: {e}")

# --- Step 3: Extract text using PyMuPDF ---
all_text = ""
for pdf_file in downloaded:
    try:
        with fitz.open(pdf_file) as doc:
            for page in doc:
                all_text += page.get_text()
        print(f"📄 Extracted text from: {pdf_file}")
    except Exception as e:
        print(f"⚠️  Failed to extract from {pdf_file}: {e}")

# --- Step 4: Save to data.txt ---
with open("data.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print("✅ All text saved to data.txt")
