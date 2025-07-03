import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import os

# Step 1: Crawl for PDF links
url = "https://www.mosdac.gov.in/data/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

pdf_links = []
for link in soup.find_all("a"):
    href = link.get("href")
    if href and "pdf" in href:
        pdf_url = "https://www.mosdac.gov.in" + href
        pdf_links.append(pdf_url)

# Create directory to save PDFs
os.makedirs("mosdac_pdfs", exist_ok=True)

# Step 2: Download and extract text
all_text = ""
for i, pdf_url in enumerate(pdf_links):
    print(f"Downloading: {pdf_url}")
    try:
        pdf_response = requests.get(pdf_url)
        filename = f"mosdac_pdfs/doc_{i+1}.pdf"
        
        with open(filename, "wb") as f:
            f.write(pdf_response.content)
        
        # Extract text using PyMuPDF
        with fitz.open(filename) as doc:
            for page in doc:
                all_text += page.get_text()
                all_text += "\n\n--- End of Page ---\n\n"
    except Exception as e:
        print(f"Error downloading {pdf_url}: {e}")

# Step 3: Save all extracted text
with open("mosdac_data.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print("\n✅ All text saved to mosdac_data.txt")
