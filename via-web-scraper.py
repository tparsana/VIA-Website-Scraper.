import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL
DETAIL_URL_PREFIX = "https://www.vatvaassociation.org/member-details-with-popupbox/?id="

# Function to get the soup object
def get_soup(url, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

# Function to extract member details from the detailed page
def get_member_details(url):
    soup = get_soup(url)
    details = {}

    try:
        # Extract the company name
        company_name_tag = soup.find('strong')
        if company_name_tag:
            details['Company Name'] = company_name_tag.text.strip()
        else:
            print(f"Company Name not found for URL: {url}")

        # Extract all paragraphs
        paragraphs = soup.find_all('p')
        for paragraph in paragraphs:
            text = paragraph.get_text()
            if ':' in text:
                key, value = text.split(':', 1)
                details[key.strip()] = value.strip()

        # Extract product and raw materials (red text)
        product_raw_material = soup.find_all('span', style="color: #a52a2a;")
        for span in product_raw_material:
            text = span.get_text().strip()
            if 'Product:' in text:
                details['Product'] = text.split(':', 1)[1].strip()
            elif 'Rawmaterial:' in text:
                details['Rawmaterial'] = text.split(':', 1)[1].strip()

    except Exception as e:
        print(f"Error extracting details from {url}: {e}")

    return details

# Function to iterate through a range of IDs and fetch member details
def collect_member_data(start_id, end_id):
    detailed_members = []
    for member_id in range(start_id, end_id + 1):
        try:
            details_url = DETAIL_URL_PREFIX + str(member_id)
            details = get_member_details(details_url)
            if details:  # Only append if details were found
                details['ID'] = member_id
                detailed_members.append(details)
            time.sleep(1)  # Respectful delay to avoid overloading the server
        except requests.exceptions.HTTPError as e:
            print(f"Failed to retrieve data for ID {member_id}: {e}")
            continue
    return detailed_members

# Save data to CSV
def save_to_csv(data, path):
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)
    print(f"Data saved to {path}")

# Main function
def main(start_id, end_id, save_path):
    member_data = collect_member_data(start_id, end_id)
    save_to_csv(member_data, save_path)

# Define the range of IDs and the save path
start_id = 1300  # Starting ID
end_id = 1310  # Ending ID (adjust as needed)
save_path = "/Users/tanishparsana/Downloads/via-web-scraper/members_details.csv"  # Update this path as needed

# Run the main function
if __name__ == "__main__":
    main(start_id, end_id, save_path)
