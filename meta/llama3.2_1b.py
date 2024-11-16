from transformers import AutoTokenizer, AutoModelForCausalLM

# Specify the model name
model_name = "meta-llama/Llama-3.2-1B"

# Load the tokenizer and model
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
except Exception as e:
    print(f"Error loading model or tokenizer: {e}")
    exit()

# Set the pad_token_id to avoid warnings
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = model.config.eos_token_id

while True:
    # Take user input
    user_input = input("Enter your prompt (or type 'exit' to quit): ")
    if user_input.lower() == "exit":
        print("Exiting...")
        break

    # Tokenize the input
    inputs = tokenizer(user_input, return_tensors="pt", padding=True)

    # Generate text based on the input
    outputs = model.generate(
        inputs['input_ids'],
        attention_mask=inputs['attention_mask'],  # Add attention mask
        max_length=100,  # Adjust max_length as needed
        temperature=0.7,  # Control randomness of the output
        num_return_sequences=1,  # Number of responses to generate
        pad_token_id=tokenizer.pad_token_id,  # Avoid warnings
    )

    # Decode and print the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Response: {generated_text}")
