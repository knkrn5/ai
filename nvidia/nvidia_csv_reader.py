import os
from dotenv import load_dotenv
from openai import OpenAI
import csv

# Load environment variables
load_dotenv()

# Initialize the OpenAI client with NVIDIA's base URL and API key
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API")
)

# Function to extract text from a CSV file
def extract_csv_text(csv_path):
    try:
        with open(csv_path, 'r') as file:
            csv_data = csv.reader(file) #reads the CSV file as a list of lists
            # Combine rows into a formatted string
            rows = [" | ".join(row) for row in csv_data]
            text = "\n".join(rows)
        return text
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return ""

# Ask for CSV file path and extract the text
csv_path = "./data/game_data.csv"
csv_text = extract_csv_text(csv_path)

if not csv_text:
    print("Failed to extract text from the CSV. Please check the file path and content.")
    exit()

print("\nCSV Text Extracted Successfully!")

while True:
    # Take user input for the question
    user_question = input("\nPlease enter your question (or type 'exit' or 'q' to quit): ")

    # Exit the loop if the user types 'exit' or 'q'
    if user_question.lower() in ['exit', 'q']:
        print("Exiting the program.")
        break

    try:
        # Create a completion request with the user question and extracted CSV text as context
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. only answer based on the provided CSV data. Do not answer any questions that are not based on the CSV data."},
                {"role": "assistant", "content": "I will answer questions only based on the provided csv data."},
                {"role": "system", "content": f"CSV Data:\n{csv_text}"},
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
        for chunk in completion:
            if hasattr(chunk.choices[0].delta, "content"):
                print(chunk.choices[0].delta.content, end="")
        print()  # For newline after the streamed response

    except Exception as e:
        print(f"Error occurred during completion request: {e}")
