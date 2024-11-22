import os
from dotenv import load_dotenv
from openai import OpenAI
from datasets import load_dataset

load_dotenv()

# Load the dataset
dataset = load_dataset("knkrn5/wealthpsychology-raw-data")

# Checking if the data has the tokenized format
print(dataset)

all_data = []

# Print details of each split in the DatasetDict
for split_name, split_data in dataset.items():
    split_df = split_data.to_pandas()
    all_data.append(split_df)
    # print(split_df.head())
    print(all_data)
    print("\n" + "="*50 + "\n")
    

# Initialize the OpenAI client with NVIDIA's base URL and API key
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API")
)

while True:
    # Take user input for the question
    user_question = input("\nPlease enter your question (or type 'exit' or 'q' to quit): ")

    # Exit the loop if the user types 'exit'
    if user_question.lower() in ['exit', 'q']:
        print("Exiting the program.")
        break

    # Create a completion request with the user question
    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[
            {"role": "system", "content": " your are an AI assistant."},
            {"role": "system", "content": f"dataset: {all_data}."},
            {"role": "user", "content": user_question}
        ],
        temperature=0.5,
        # top_k = 50,
        top_p=0.7,
        max_tokens=1024,
        # repetition_penalty=1.2,
        stream=True
    )

    # Stream the response chunks and print them
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")