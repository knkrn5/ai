import os
from dotenv import load_dotenv
from openai import OpenAI
from urllib.parse import urlparse
import requests
import json
from bs4 import BeautifulSoup  # For parsing HTML content

# Load environment variables
load_dotenv()

# Initialize the OpenAI client with NVIDIA's base URL and API key
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API")
)

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
                
            
# with open("website_text", "r", encoding="utf-8") as textFile:
text_data = website_text

    
while True:
    # Take user input for questions about the URL
    user_question = input("\nPlease enter your question about the URL (or type 'exit' to 'q'): ")
    
    if user_question.lower() in ['exit', 'q']:
        print("Exiting the program.")
        break
        
    try:
        # Create a completion request
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Use the provided URL data to answer questions. Do not answer any questions that are not based on the URL data."}, 
                {"role": "assistant", "content": "I will only answer based on the provided data."},
                {"role": "system", "content": f"URL Data:\n{text_data}"},
                {"role": "user", "content": user_question}
            ],
            temperature=0.5,
            top_p=0.7,
            max_tokens=1024,
            stream=True
        )
        
        # Stream the response chunks and print them
        print("\nAI Response:")
        full_response = ""
        for chunk in completion:
            if hasattr(chunk.choices[0].delta, "content"):
                content = chunk.choices[0].delta.content or ""
                full_response += content
                print(content, end="")
        print()  # Newline after response
        
    except Exception as e:
        print(f"Error occurred during completion request: {e}")
