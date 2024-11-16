from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Use more CPU threads if running on CPU
torch.set_num_threads(10)  

# Specify the model name
model_name = "Qwen/Qwen2.5-1.5B-Instruct" 

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Set the pad_token_id to avoid warnings
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = model.config.eos_token_id

# Move model to GPU if available
# device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"
model = model.to(device)

while True:
    # Take user input
    user_input = input("Enter your prompt (or type 'exit' or 'q' to quit): ")
    if user_input.lower() in ["exit", 'q']:
        print("Exiting...")
        break

    # Tokenize the input
    inputs = tokenizer(user_input, return_tensors="pt", padding=True).to(device)

    # Generate text based on the input
    outputs = model.generate(
        inputs['input_ids'],
        attention_mask=inputs['attention_mask'],  # Add attention mask
        max_length=200,  #max_length as needed
        temperature=0.5,  #randomness of the output
        num_return_sequences=1,  # Number of responses to generate
        pad_token_id=tokenizer.pad_token_id,  # Avoid warnings
    )

    # Decode and print the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Response: {generated_text}")
