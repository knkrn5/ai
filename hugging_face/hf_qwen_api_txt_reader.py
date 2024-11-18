import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

client = InferenceClient(api_key=os.getenv("HUGGING_FACE_API"))

txt_path = "./data/document.txt"

with open(txt_path, "r", encoding="utf-8") as file:
    txt_content = file.read()
    print(txt_content)
    
    
if not txt_content:
    print("Failed to extract text from the txt. Please check the file path and content.")
    exit()
    

while True:
	user_input = input("\nAsk the question or type 'exit' or 'q' to quit: ")

	if user_input.lower() in ["exit", 'q']:
		print("Exiting...")
		break

	messages = [
        {"role": "system","content": f"Text Data:\n{txt_content}"},
        {"role": "user","content": user_input}
	]

	stream = client.chat.completions.create(
		model="Qwen/Qwen2.5-1.5B-Instruct", 
		messages=messages, 
		max_tokens=200,
		stream=True
	)

	for chunk in stream:
		print(chunk.choices[0].delta.content, end="")