import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
from bs4 import BeautifulSoup  # For parsing HTML content

# Load environment variables
load_dotenv()

urls = ["https://wealthpsychology.in/index.html",
        "https://wealthpsychology.in/blog/",
        "https://wealthpsychology.in/financial-calculators/",
        "https://wealthpsychology.in/finance-quizzes/",
        "https://wealthpsychology.in/contact-us/"
    ]

all_data = []

# Initialize the OpenAI client with NVIDIA's base URL and API key
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API")
)

def extract_all_text(urls):
    try:
        # Send a GET request to the URL
        for url in urls:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for HTTP errors

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract all text
            text = soup.get_text(separator="\n")  # Separate text blocks with newlines

            # Remove extra newlines
            cleaned_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
            
            # Append cleaned text to the list
            all_data.append(cleaned_text)

        return "\n\n".join(all_data)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return None

# calling function
website_text = extract_all_text(urls)

print("Extracted Text successfully from the Website:")
                
            
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
            # repetition_penalty=1.2,
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
