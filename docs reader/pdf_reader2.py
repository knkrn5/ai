import pdfplumber
from transformers import pipeline

# Initialize the summarization pipeline (using BART model)
summarizer = pipeline("summarization")

# Function to extract text from the PDF using pdfplumber
def read_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to split large text into smaller chunks
def split_text(text, max_length=1024):
    # Split the text into chunks of the specified max length
    chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    return chunks

# Function to summarize the content of the PDF
def summarize_pdf(pdf_path):
    document = read_pdf(pdf_path)  # Calling the read_pdf function to extract text
    text_chunks = split_text(document)  # Split the document into smaller chunks
    summary = ""
    
    # Summarize each chunk
    for chunk in text_chunks:
        chunk_summary = summarizer(chunk, max_length=200, min_length=50, do_sample=False)
        summary += chunk_summary[0]['summary_text'] + " "
    
    return summary.strip()

# Example usage
summary = summarize_pdf("economic.pdf")
print("Summary:", summary)
