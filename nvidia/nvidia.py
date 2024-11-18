import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

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
            {"role": "user", "content": user_question}
        ],
        temperature=0.5,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )

    # Stream the response chunks and print them
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")