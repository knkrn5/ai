from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
tokenizer.clean_up_tokenization_spaces = False

model = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad")

# Set up the pipeline with the model and tokenizer
pipe = pipeline(
    "question-answering",
    model=model,
    tokenizer=tokenizer
)

# Read document (context) from an external file
with open("document.txt", "r") as file:
    document = file.read()

# List of questions you want to ask
questions = [
    "What does Hugging Face Inc. develop?",
    "What is Hugging Face most famous for?",
    "Is Elon Musk involved in human?"
]

# Loop through questions and get answers
for question in questions:
    result = pipe(question=question, context=document)
    print(f"Question: {question}")
    print(f"Answer: {result['answer']}\n")
