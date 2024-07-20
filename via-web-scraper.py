import requests
from bs4 import BeautifulSoup
import csv

# Define the base URL and the range of IDs to iterate through
base_url = "https://www.vatvaassociation.org/member-details-with-popupbox/?id="
start_id = 1400
end_id = 1410  # Adjust this range as needed

# Define the output CSV file
output_file = "/Users/tanishparsana/Downloads/Projects/VIA-website-scraper/company_data.csv"

# Define the schema for the CSV file
fieldnames = ["Company name", "Member No", "Category", "Year of Established", "Address", "Phone", "Fax", "Email", "Website", "Executive", "Mobile", "Product", "Rawmaterial"]

# Function to fetch and convert the page to text
def fetch_page_text(url):
    try:
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text(separator='\n')
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from {url} with error: {e}")
        return None

# Function to extract data from the readable text
def extract_data_from_text(text):
    data = {key: "" for key in fieldnames}
    
    lines = text.split('\n')
    address_lines = []
    for i, line in enumerate(lines):
        line = line.strip()
        if "Member No:" in line:
            data["Member No"] = line.split(":", 1)[1].strip()
        elif "Category:" in line:
            data["Category"] = line.split(":", 1)[1].strip()
        elif "Year of Established:" in line:
            data["Year of Established"] = line.split(":", 1)[1].strip()
        elif "Address:" in line:
            address_start = i + 1
            while address_start < len(lines) and not any(keyword in lines[address_start] for keyword in ["Phone:", "Fax:", "Email:", "Website:", "Executive:", "Mobile:", "Product:", "Rawmaterial:"]):
                address_lines.append(lines[address_start].strip())
                address_start += 1
            data["Address"] = ' '.join(address_lines)
        elif "Phone:" in line:
            data["Phone"] = line.split(":", 1)[1].strip()
        elif "Fax:" in line:
            data["Fax"] = line.split(":", 1)[1].strip()
        elif "Email:" in line:
            data["Email"] = line.split(":", 1)[1].strip()
        elif "Website:" in line:
            data["Website"] = line.split(":", 1)[1].strip()
        elif "Executive:" in line:
            data["Executive"] = line.split(":", 1)[1].strip()
        elif "Mobile:" in line:
            data["Mobile"] = line.split(":", 1)[1].strip()
        elif "Product:" in line:
            data["Product"] = line.split(":", 1)[1].strip()
        elif "Rawmaterial:" in line:
            data["Rawmaterial"] = line.split(":", 1)[1].strip()
        elif line and not any(k in line for k in ["Member No:", "Category:", "Year of Established:", "Address:", "Phone:", "Fax:", "Email:", "Website:", "Executive:", "Mobile:", "Product:", "Rawmaterial:"]):
            data["Company name"] = line.strip()
    
    return data

# Open the CSV file for writing
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through the range of IDs
    for company_id in range(start_id, end_id + 1):
        url = base_url + str(company_id)
        page_text = fetch_page_text(url)
        if page_text:
            data = extract_data_from_text(page_text)
            writer.writerow(data)
            print(f"Successfully scraped data for company ID: {company_id}")

print("Scraping completed.")
