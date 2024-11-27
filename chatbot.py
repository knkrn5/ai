from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize Flask and OpenAI
app = Flask(__name__)
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API")
)

@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    user_question = data.get("question")

    if not user_question:
        return jsonify({"error": "Question is required"}), 400

    try:
        # Create a completion request
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": user_question}
            ],
            temperature=0.5,
            top_p=0.7,
            max_tokens=1024,
            stream=False
        )

        # Aggregate the response
        response_text = "".join(chunk.choices[0].text for chunk in completion)

        return jsonify({"response": response_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
