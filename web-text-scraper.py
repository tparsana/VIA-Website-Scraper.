import requests
from bs4 import BeautifulSoup

def scrape_webpage(url, file_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from the webpage
        page_text = soup.get_text()

        # Save the extracted text to a file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(page_text)

        print(f"Data successfully scraped and saved to {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error during requests to {url}: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
url = 'https://www.vatvaassociation.org/member-details-with-popupbox/?id=1450'  # Replace with your URL
file_path = '/Users/tanishparsana/Downloads/Projects/VIA-website-scraper/webpage_data.txt'   # Replace with your desired file path
scrape_webpage(url, file_path)
