from datasets import load_dataset

# Load the Hugging Face dataset
dataset = load_dataset("fka/awesome-chatgpt-prompts")
# df = pd.read_csv("hf://datasets/fka/awesome-chatgpt-prompts/prompts.csv")
# dataset = load_dataset("fka/awesome-chatgpt-prompts", data_files={"train": "prompts.csv"})


# Access the specific CSV file in the dataset
df = dataset['train'].to_pandas()  # Convert to a Pandas DataFrame
