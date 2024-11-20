import pdfplumber
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering

# Initialize the question-answering pipeline
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
model = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad")
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)

# Function to extract text from the PDF using pdfplumber
def read_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to answer a question based on the PDF content
def answer_question_from_pdf(pdf_path, question):
    document = read_pdf(pdf_path)
    result = qa_pipeline(question=question, context=document)
    return result['answer']

# Example usage:
pdf_path = "economic.pdf"
question = "what is economics"
answer = answer_question_from_pdf(pdf_path, question)
print("Answer:", answer)
