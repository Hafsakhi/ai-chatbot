from flask import Flask, request, jsonify, send_from_directory
import openai
from dotenv import load_dotenv

load_dotenv()
import os

app = Flask(__name__)

# ---- CONFIG AZURE OPENAI ----
openai.api_type = "azure"
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = "https://sakhi-mhud29zh-eastus2.cognitiveservices.azure.com/"
openai.api_version = "2024-02-01"
deployment_name = "chatbot-model-openai"
openai.api_key = AZURE_OPENAI_KEY

# ---- ROUTE FRONT-END ----
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# ---- ROUTE API CHATBOT ----
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    response = openai.ChatCompletion.create(
        engine=deployment_name,
        messages=[{"role": "user", "content": user_input}],
        max_tokens=200
    )

    bot_reply = response["choices"][0]["message"]["content"]
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
