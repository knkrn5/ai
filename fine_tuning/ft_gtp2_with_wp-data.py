from datasets import load_dataset, concatenate_datasets
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling

# Load the dataset
dataset = load_dataset("knkrn5/wealthpsychology-tokenized-data")

# Check if the data has the tokenized format
print(dataset)

model_name = "gpt2"

# Define the model
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Setting the pad_token_id to the eos_token_id to avoid warnings and errors
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = model.config.eos_token_id

# Define the training arguments
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=4,
    num_train_epochs=5,
    save_strategy="epoch",  # Save model after each epoch
    load_best_model_at_end=True,  # Load the best model based on eval loss
)


# Prepare the dataset
def preprocess_function(examples):
    return {
        "input_ids": examples["input_ids"],
        "attention_mask": examples["attention_mask"]
    }

# Apply the preprocessing function
tokenized_datasets = dataset.map(preprocess_function, batched=True)

# Concatenate datasets for training and evaluation
train_dataset = concatenate_datasets([tokenized_datasets["wp_pages"], tokenized_datasets["blog_categories"], tokenized_datasets["fin_calculators"], tokenized_datasets["fin_quizzes"]])
eval_dataset = concatenate_datasets([tokenized_datasets["wp_home"], tokenized_datasets["contact_info"], tokenized_datasets["about_us"], tokenized_datasets["our_team"], tokenized_datasets["our_plan"]])

# Define the data collator for language modeling (handles padding)
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,  # GPT-2 does not use masked language modeling
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=data_collator,  # Use the data collator for padding
)

# Start the training process
trainer.train()

model.save_pretrained("./final_model")
tokenizer.save_pretrained("./final_model")
