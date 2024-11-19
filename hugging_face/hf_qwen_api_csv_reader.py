import os
import csv
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

client = InferenceClient(api_key=os.getenv("HUGGING_FACE_API"))

# List to store rows as dictionaries
csv_files = ['wp-csv-data/wp-pages.csv', 
            'wp-csv-data/wp-home.csv', 
            'wp-csv-data/blog-categories.csv', 
            'wp-csv-data/fin-calculators.csv', 
            'wp-csv-data/fin-quizzes.csv', 
            'wp-csv-data/contact-info.csv', 
            'wp-csv-data/about-us.csv', 
            'wp-csv-data/our-team.csv', 
            'wp-csv-data/our-plan.csv'
            ]

# txt_path = "./data/document.txt"
all_data = []  # List to store combined data from all files
for csv_data in csv_files:
    try:
        with open(csv_data, 'r', encoding='utf-8') as file:
            csv_content = csv.DictReader(file)
            for row in csv_content:
                all_data.append(row)
    except Exception as e:
        print(f"Error reading CSV file {csv_data}: {e}")
            
            
# Extract text from CSV files
csv_data_str = f"\n{all_data}"
        

if not csv_data_str:
    print("Failed to extract text from the csv. Please check the file path and content.")
    exit()
    
print("csv read successfully")

    

while True:
	user_input = input("\nAsk the question or type 'exit' or 'q' to quit: ")

	if user_input.lower() in ["exit", 'q']:
		print("Exiting...")
		break


	stream = client.chat.completions.create(
		model="Qwen/Qwen2.5-1.5B-Instruct", 
		messages = [
        {"role": "system", "content": "You are a helpful assistant. Only answer based on the provided text data. Do not answer any questions that are not based on the text data."},
        {"role": "system","content": f"Text Data:\n{csv_data_str}"},
        {"role": "assistant", "content": "I will only answer questions only based on the provided text data."},
        {"role": "user","content": user_input}
        ], 
		temperature=0.5,
        top_p=0.7,
        max_tokens=1024,
        stream=True
	)

	for chunk in stream:
		print(chunk.choices[0].delta.content, end="")