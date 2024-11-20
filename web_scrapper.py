import requests
from bs4 import BeautifulSoup

def extract_all_text(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all text
        text = soup.get_text(separator="\n")  # Separate text blocks with newlines

        # Remove extra newlines
        cleaned_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

        return cleaned_text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return None

# Replace 'your-website-url' with the URL of your website
url = "https://wealthpsychology.in/index.html"
website_text = extract_all_text(url)

if website_text:
    print("Extracted Text from the Website:")
    print(website_text)
    # Optionally, save to a file
    """  with open("website_text.txt", "w", encoding="utf-8") as file:
            file.write(website_text)
            print("\nText has been saved to 'website_text.txt'.") """
