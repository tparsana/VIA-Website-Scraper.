import requests
from bs4 import BeautifulSoup
import csv

# Define the base URL and the range of IDs to iterate through
base_url = "https://www.vatvaassociation.org/member-details-with-popupbox/?id="
start_id = 1400
end_id = 1410  # Adjust this range as needed

# Define the output CSV file
output_file = "/Users/tanishparsana/Downloads/Projects/via-web-scraper/company_data.csv"

# Define the schema for the CSV file
fieldnames = ["Company name", "Member No", "Category", "Year of Established", "Address", "Phone", "Fax", "Email", "Website", "Executive", "Mobile", "Product", "Rawmaterial"]

def extract_data_from_text(text):
    data = {
        "Company name": "",
        "Member No": "",
        "Category": "",
        "Year of Established": "",
        "Address": "",
        "Phone": "",
        "Fax": "",
        "Email": "",
        "Website": "",
        "Executive": "",
        "Mobile": "",
        "Product": "",
        "Rawmaterial": ""
    }
    
    lines = text.split('\n')
    address_lines = []
    capture_address = False

    for line in lines:
        line = line.strip()
        if line.startswith("Member No:"):
            data["Member No"] = line.split(":", 1)[1].strip()
        elif line.startswith("Category:"):
            data["Category"] = line.split(":", 1)[1].strip()
        elif line.startswith("Year of Established:"):
            data["Year of Established"] = line.split(":", 1)[1].strip()
        elif line.startswith("Address:"):
            capture_address = True
        elif capture_address:
            if line.startswith(("Phone:", "Fax:", "Email:", "Website:", "Executive:", "Mobile:", "Product:", "Rawmaterial:")):
                capture_address = False
            else:
                address_lines.append(line)
        elif line.startswith("Phone:"):
            data["Phone"] = line.split(":", 1)[1].strip()
        elif line.startswith("Fax:"):
            data["Fax"] = line.split(":", 1)[1].strip()
        elif line.startswith("Email:"):
            data["Email"] = line.split(":", 1)[1].strip()
        elif line.startswith("Website:"):
            data["Website"] = line.split(":", 1)[1].strip()
        elif line.startswith("Executive:"):
            data["Executive"] = line.split(":", 1)[1].strip()
        elif line.startswith("Mobile:"):
            data["Mobile"] = line.split(":", 1)[1].strip()
        elif line.startswith("Product:"):
            data["Product"] = line.split(":", 1)[1].strip()
        elif line.startswith("Rawmaterial:"):
            data["Rawmaterial"] = line.split(":", 1)[1].strip()
        elif line and not any(k in line for k in fieldnames[1:]):
            data["Company name"] = line

    data["Address"] = ' '.join(address_lines)
    return data

# Open the CSV file for writing
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through the range of IDs
    for company_id in range(start_id, end_id + 1):
        url = base_url + str(company_id)
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator='\n')
            data = extract_data_from_text(text)
            writer.writerow(data)
            print(f"Successfully scraped data for company ID: {company_id}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to scrape data for company ID: {company_id} with error: {e}")

print("Scraping completed.")
