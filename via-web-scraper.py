import requests
from bs4 import BeautifulSoup
import csv
import re

def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

def parse_text(text):
    lines = text.splitlines()
    first_non_empty_line = next((line.strip() for line in lines if line.strip()), "N/A")
    
    data = {}
    schema = [
        "Company Name:",
        "Member No:",
        "Category:",
        "Year of Established:",
        "Address:",
        "Phone:",
        "Fax:",
        "Email:",
        "Website:",
        "Executive:",
        "Mobile:",
        "Product:",
        "Rawmaterial:"
    ]
    
    # Set the first non-empty line as the company name
    data["Company Name:"] = first_non_empty_line
    
    for field in schema[1:]:
        pattern = re.compile(f"\\s*{re.escape(field)}\\s*(.*)")
        matches = pattern.findall(text)
        if matches:
            # Concatenate multiple matches if there are more than one
            data[field] = ' | '.join(match.strip() for match in matches)
        else:
            data[field] = "N/A"
    
    return data

def save_text_to_csv(data_list, filename):
    schema = [
        "Serial Number",
        "Company Name:",
        "Member No:",
        "Category:",
        "Year of Established:",
        "Address:",
        "Phone:",
        "Fax:",
        "Email:",
        "Website:",
        "Executive:",
        "Mobile:",
        "Product:",
        "Rawmaterial:"
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(schema)  # Write header row
        for data in data_list:
            writer.writerow([data.get(field, "N/A") for field in schema])

if __name__ == "__main__":
    base_url = "https://www.vatvaassociation.org/member-details-with-popupbox/?id="
    start_id = int(input("Enter the starting serial number: "))
    end_id = int(input("Enter the ending serial number: "))
    
    all_data = []
    
    for company_id in range(start_id, end_id + 1):
        url = f"{base_url}{company_id}"
        text = extract_text_from_url(url)
        data = parse_text(text)
        data["Serial Number"] = company_id  # Add the serial number to the data
        all_data.append(data)
    
    save_text_to_csv(all_data, 'output.csv')

## Serial No. Start: 1271
## Serial No. End: 2530
## Total Serial Nos.: 1259 Companies