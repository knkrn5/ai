import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-405B"
headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API')}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "Can you please let us know more details about your ",
})
print(output)