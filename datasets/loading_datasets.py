from datasets import load_dataset
# from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments

# Load the dataset
dataset = load_dataset("knkrn5/wealthpsychology-tokenized-data")

# Check if the data has the tokenized format
print(dataset)
print(dataset["wp_pages"])  # To check one split
print(dataset.column_names)

