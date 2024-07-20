import requests
from bs4 import BeautifulSoup
import csv
import re

def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

def parse_text(text):
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
    
    for field in schema:
        pattern = re.compile(f"{field}\s*(.*)")
        match = pattern.search(text)
        if match:
            data[field] = match.group(1).strip()
        else:
            data[field] = "N/A"
    
    return data

def save_text_to_csv(data, filename):
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
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for field in schema:
            writer.writerow([field, data[field]])

if __name__ == "__main__":
    url = input("Enter the URL: ")
    text = extract_text_from_url(url)
    data = parse_text(text)
    save_text_to_csv(data, 'output.csv')
