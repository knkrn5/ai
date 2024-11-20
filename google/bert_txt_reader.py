# Load model directly
from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch

#if running on CPU
torch.set_num_threads(100)

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
model = AutoModelForMaskedLM.from_pretrained("google-bert/bert-base-uncased")


# Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)


# Read document (context) from an external file
with open("data/document.txt", "r") as file:
    document = file.read()

while True:
    
    # List of questions you want to ask
    user_input = input("\nAsk the question or type 'exit' or 'q' to quit: ")
    
    if user_input.lower() in ["exit", 'q']:
        print("Exiting...")
        break

    # Loop through questions and get answers
    print(f"Question: {user_input}")
    print(f"Answer: {result['answer']}\n")
