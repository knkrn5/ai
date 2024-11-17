import os
from huggingface_hub import InferenceClient

client = InferenceClient(api_key=os.getenv("hugging_face_api"))

user_input = input("Ask the question or type 'exit' or 'q' to quit: ")

messages = [
	{
		"role": "user",
		"content": user_input
	}
]

stream = client.chat.completions.create(
    model="Qwen/Qwen2.5-1.5B-Instruct", 
	messages=messages, 
	max_tokens=500,
	stream=True
)

for chunk in stream:
    print(chunk.choices[0].delta.content, end="")