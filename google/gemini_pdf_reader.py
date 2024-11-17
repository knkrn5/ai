import os
import google.generativeai as genai
import PyPDF2
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API"))
model = genai.GenerativeModel("gemini-1.5-flash")  # Create model instance

def extract_pdf_text(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return None

def ask_question():
    while True:
        user_question = input("\nPlease ask your question (or type 'exit' to quit): ").strip()
        if user_question.lower() in ['exit', 'q']:
            return None
        if not user_question:
            print("Error: Question cannot be empty. Please try again.")
        else:
            return user_question

def generate_response(pdf_text, user_question):
    try:
        prompt = f"Based on the following document:\n\n{pdf_text}\n\nPlease answer the question: {user_question}"
        response = model.generate_content(prompt)  # Use model instance
        return response.text
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return None

# Main loop
if __name__ == "__main__":
    pdf_path = "./data/economic.pdf"
    pdf_text = extract_pdf_text(pdf_path)
    
    if pdf_text:
        print("PDF text extracted successfully.")
        while True:
            user_question = ask_question()
            if not user_question:
                break
            response = generate_response(pdf_text, user_question)
            if response:
                print(f"\nResponse:\n{response}")
    else:
        print("Error: Failed to extract text from PDF.")