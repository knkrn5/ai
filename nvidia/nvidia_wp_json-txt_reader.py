import os
from dotenv import load_dotenv
from openai import OpenAI
import json

# Load environment variables
load_dotenv()

# List of JSON files to process
json_files = [
    'data/wp-json-data/wp-pages.json',
    'data/wp-json-data/wp-home.json',
    'data/wp-json-data/blog-categories.json',
    'data/wp-json-data/fin-calculators.json',
    'data/wp-json-data/fin-quizzes.json',
    'data/wp-json-data/contact-info.json',
    'data/wp-json-data/about-us.json',
    'data/wp-json-data/our-team.json',
    'data/wp-json-data/our-plan.json'
]

text_file = "data/wp-txt-data/about-me.txt"

# Initialize the OpenAI client with NVIDIA's base URL and API key
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API")
)

# Function to extract text from JSON files
def extract_json_txt_data(json_files, text_file):
    all_data = []
    try:
        # Read the text file content first
        with open(text_file, 'r', encoding='utf-8') as textFile:
            text_content = textFile.read()

        # Process each JSON file
        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as jsonFile:
                json_data = json.load(jsonFile)
                # Append each JSON entry along with text content
                for row in json_data:
                    all_data.append({
                        'json_entry': row,
                        'text_content': text_content
                    })
    except Exception as e:
        print(f"Error reading files: {e}")
    
    return all_data

# Extract text from JSON files
json_text_data = extract_json_txt_data(json_files, text_file)

if not json_text_data:
    print("Failed to extract text from the JSON or TXT. Please check the file paths and content.")
    exit()

print("\nJSON Text Extracted Successfully!")

# Convert combined data to text format for the model
json_text_data_str = json.dumps(json_text_data, indent=2)

# Main interaction loop
while True:
    # Take user input for the question
    user_question = input("\nPlease enter your question (or type 'exit' or 'q' to quit): ")
    
    # Exit the loop if the user types 'exit' or 'q'
    if user_question.lower() in ['exit', 'q']:
        print("Exiting the program.")
        break
    
    try:
        # Create a completion request with the user question and extracted JSON text as context
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Only answer based on the provided JSON data. Do not answer any questions that are not based on the JSON data."},
                {"role": "assistant", "content": "I will only answer questions only based on the provided JSON data."},
                {"role": "system", "content": f"JSON Data:\n{json_text_data_str}"},
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
        print()  # For newline after the streamed response
    
    except Exception as e:
        print(f"Error occurred during completion request: {e}")