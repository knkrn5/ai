import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API"))
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_question():
    user_question = input("\nPlease ask your question (or type 'exit' to quit): ")
    if user_question.lower() in ['exit', 'q']:
        print("Exiting...")
        return False
    return user_question

while True:
    user_question = ask_question()
    if not user_question:
        break

    try:
        response = model.generate_content(
            user_question,
            generation_config=genai.types.GenerationConfig(max_output_tokens=1024),
            stream=True
            )
        for chunk in response:
                print(chunk.text, end='')
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please try again or check your API key and internet connection.")