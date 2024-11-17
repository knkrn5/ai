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

# Function to parse CSV data into a list of dictionaries
def parse_csv_data(csv_path):
    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        return data
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

# Function to check if a question can be answered from the CSV data
def validate_question(question, csv_data):
    # Example: Simple validation to check if a keyword in the question matches a column or row
    question_lower = question.lower()
    for row in csv_data:
        if any(question_lower in str(value).lower() for value in row.values()):
            return False
    return True

# Load and parse the CSV data
csv_path = "./data/game_data.csv"
csv_data = parse_csv_data(csv_path)

if not csv_data:
    print("Failed to parse the CSV. Please check the file path and content.")
    exit()

print("\nCSV Data Loaded Successfully!")

while True:
    # Take user input for the question
    user_question = input("\nPlease enter your question (or type 'exit' or 'q' to quit): ")

    # Exit the loop if the user types 'exit' or 'q'
    if user_question.lower() in ['exit', 'q']:
        print("Exiting the program.")
        break

    # Validate the question against the CSV data
    if not validate_question(user_question, csv_data):
        print("Sorry, I can only answer questions based on the CSV data provided.")
        continue

    try:
        # Prepare the CSV data as a string for the AI
        csv_text = "\n".join([" | ".join(row.values()) for row in csv_data])

        # Create a completion request with the validated question and CSV data
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Only use the provided CSV data to answer the user's question. Do not answer if the data is unavailable."},
                {"role": "system", "content": f"CSV Data:\n{csv_text}"},
                {"role": "user", "content": user_question}
            ],
            temperature=0.5,
            top_p=0.7,
            max_tokens=1024,
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
