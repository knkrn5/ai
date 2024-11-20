
# Read the content of the text file
file_path = "data/document.txt"

with open(file_path, "r", encoding="utf-8") as file:
    data = file.read()

# Function to search for answers
def find_answer(keyword):
    if keyword.lower() in data.lower():
        return f"Keyword '{keyword}' found in the document."
    else:
        return f"Keyword '{keyword}' not found in the document."

# Example questions
print(find_answer("binance"))
print(find_answer("database"))


# Predefined questions and answers
predefined_questions = {
    "What is Binance?": "Binance is a cryptocurrency exchange platform mentioned in the document.",
    "What is a database?": "A database is a structured collection of data that is stored and accessed electronically.",
}

# Function to find predefined answers
def predefined_answer(question):
    if question in predefined_questions:
        return predefined_questions[question]
    else:
        return "Sorry, I don't have a predefined answer for that question."

# Example questions
question1 = "What is Binance?"
question2 = "What is a database?"
question3 = "What is Python?"

print(f"Q: {question1}\nA: {predefined_answer(question1)}\n")
print(f"Q: {question2}\nA: {predefined_answer(question2)}\n")
print(f"Q: {question3}\nA: {predefined_answer(question3)}\n")