import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_webpage_to_csv(url, csv_file_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from the webpage
        page_text = soup.get_text()

        # Process the text according to the schema
        lines = page_text.strip().split("\n")
        data = {
            "Company Name": lines[0].strip(),
            "Member No": lines[1].split(": ")[1].strip(),
            "Category": lines[2].split(": ")[1].strip(),
            "Year of Established": lines[3].split(": ")[1].strip(),
            "Address": lines[4].split(": ")[1].strip(),
            "Phone": lines[5].split(": ")[1].strip(),
            "Fax": lines[6].split(": ")[1].strip(),
            "Email": lines[7].split(": ")[1].strip(),
            "Website": lines[8].split(": ")[1].strip(),
            "Executive": [lines[9].split(": ")[1].strip(), lines[11].split(": ")[1].strip()],
            "Mobile": [lines[10].split(": ")[1].strip(), lines[12].split(": ")[1].strip()],
            "Product": lines[13].split(": ")[1].strip(),
            "Rawmaterial": lines[14].split(": ")[1].strip(),
        }

        # Create a DataFrame
        df = pd.DataFrame({
            "Company Name": [data["Company Name"]],
            "Member No": [data["Member No"]],
            "Category": [data["Category"]],
            "Year of Established": [data["Year of Established"]],
            "Address": [data["Address"]],
            "Phone": [data["Phone"]],
            "Fax": [data["Fax"]],
            "Email": [data["Email"]],
            "Website": [data["Website"]],
            "Executive": [", ".join(data["Executive"])],
            "Mobile": [", ".join(data["Mobile"])],
            "Product": [data["Product"]],
            "Rawmaterial": [data["Rawmaterial"]],
        })

        # Save the DataFrame to a CSV file
        df.to_csv(csv_file_path, index=False)

        print(f"Data successfully scraped and saved to {csv_file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error during requests to {url}: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
url = 'https://www.vatvaassociation.org/member-details-with-popupbox/?id=1450'  # Replace with your URL
csv_file_path = '/Users/tanishparsana/Downloads/Projects/VIA-website-scraper/company-data.csv'  # Replace with your desired file path
scrape_webpage_to_csv(url, csv_file_path)
