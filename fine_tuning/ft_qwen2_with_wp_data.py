import os
from datasets import load_dataset, concatenate_datasets
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)
import torch

# Environment variables
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"  # To avoid fragmentation
os.environ["WANDB_DISABLED"] = "true"

# Load the dataset
dataset = load_dataset("knkrn5/wealthpsychology-tokenized-data")

print(dataset)

# Load Qwen model and tokenizer
model_name = "Qwen/Qwen2.5-1.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Enable gradient checkpointing to save memory
model.gradient_checkpointing_enable()

# Ensure pad_token is set to eos_token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = model.config.eos_token_id

# Move the model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Define the training arguments
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=2,  # Reduced batch size
    gradient_accumulation_steps=2,  # Simulate larger batch size
    num_train_epochs=5,
    save_strategy="epoch",
    logging_dir="./logs",
    logging_steps=10,
    load_best_model_at_end=True,
    save_total_limit=3,
    fp16=True,  # Mixed precision training
)

# Preprocessing function for the dataset
def preprocess_function(examples):
    return {
        "input_ids": examples["input_ids"],
        "attention_mask": examples["attention_mask"]
    }

# Apply the preprocessing function
tokenized_datasets = dataset.map(preprocess_function, batched=True)

# Split the datasets into train and eval datasets
train_dataset = concatenate_datasets([
    tokenized_datasets["wp_pages"],
    tokenized_datasets["blog_categories"],
    tokenized_datasets["fin_calculators"],
    tokenized_datasets["fin_quizzes"]
])
eval_dataset = concatenate_datasets([
    tokenized_datasets["wp_home"],
    tokenized_datasets["contact_info"],
    tokenized_datasets["about_us"],
    tokenized_datasets["our_team"],
    tokenized_datasets["our_plan"]
])

# Define the data collator for causal language modeling
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=data_collator,
    tokenizer=tokenizer,
)

# Start training
trainer.train()

# Save the final model and tokenizer
model.save_pretrained("./final_model")
tokenizer.save_pretrained("./final_model")
