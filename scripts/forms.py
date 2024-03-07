import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Desktop path to save the files
desktop_path = r"C:\Users\PMD - FEMI\OneDrive\Desktop\USCIS"

def download_pdf(pdf_url):
    response = requests.get(pdf_url)
    
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to download PDF from {pdf_url}")
        return None

def extract_info_and_save(pdf_content, output_path):
    # Modify this function based on your specific PDF information extraction requirements
    # This example just saves the PDF to the specified output path
    with open(output_path, 'wb') as output_file:
        output_file.write(pdf_content)

def main():
    urls = ["https://www.uscis.gov/i-765", "https://www.uscis.gov/i-90", "https://www.uscis.gov/n-400",
            "https://www.uscis.gov/i-129f", "https://www.uscis.gov/i-130", "https://www.uscis.gov/i-360",
            "https://www.uscis.gov/i-600", "https://www.uscis.gov/i-751", "https://www.uscis.gov/i-9",
            "https://www.uscis.gov/i-129", "https://www.uscis.gov/i-140", "https://www.uscis.gov/i-526",
            "https://www.uscis.gov/i-539", "https://www.uscis.gov/i-134a", "https://www.uscis.gov/i-589",
            "https://www.uscis.gov/i-730", "https://www.uscis.gov/i-821"]
    
    for url in urls:
        # Make a request to the URL and get the HTML content
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.content
        else:
            print(f"Failed to retrieve HTML from {url}")
            continue

        # Parse HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all PDF links on the page
        pdf_links_elements = soup.find_all('a', {'href': lambda href: href and href.endswith('.pdf')})

        if pdf_links_elements:
            for pdf_link_element in pdf_links_elements:
                pdf_url = urljoin(url, pdf_link_element.get('href'))
                pdf_content = download_pdf(pdf_url)

                if pdf_content:
                    # Get the filename from the PDF link
                    pdf_filename = os.path.basename(urlparse(pdf_url).path)
                    output_path = os.path.join(desktop_path, pdf_filename)
                    extract_info_and_save(pdf_content, output_path)
                    print(f"PDF successfully downloaded and saved at: {output_path}")
                else:
                    print(f"Failed to download PDF from {pdf_url}")
        else:
            print(f"No PDF links found on the page: {url}")

if __name__ == "__main__":
    main()
