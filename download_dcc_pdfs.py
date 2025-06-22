import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "https://cannabis.ca.gov/resources/rules-and-regulations/"
DOWNLOAD_DIR = "./docs"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_dcc_pdfs():
    print("Fetching DCC regulation page...")
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = soup.find_all('a', href=True)
    pdf_links = [link['href'] for link in links if link['href'].endswith('.pdf')]

    print(f"Found {len(pdf_links)} PDF links.")

    for url in pdf_links:
        filename = url.split("/")[-1]
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        if not os.path.exists(filepath):
            print(f"Downloading {filename}...")
            pdf_data = requests.get(url).content
            with open(filepath, 'wb') as f:
                f.write(pdf_data)
        else:
            print(f"{filename} already exists, skipping.")

    print("Download complete.")

if __name__ == "__main__":
    download_dcc_pdfs()
