import pdfplumber
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering

# Initialize the question-answering pipeline (using DistilBERT model)
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Function to extract text from the PDF using pdfplumber
def read_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to answer a question based on the PDF document
def answer_question(pdf_path, question):
    document = read_pdf(pdf_path)  # Extract text from PDF
    result = qa_pipeline(question=question, context=document)  # Use the QA pipeline
    return result['answer']

# Example usage
question = "how to be productive"
answer = answer_question("economic.pdf", question)
print("Question:", question)
print("Answer:", answer)
