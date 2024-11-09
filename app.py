from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import time

app = Flask(__name__)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Store chat history
chat_history = []

@app.route("/")
def index():
    return render_template("index.html", messages=chat_history)

@app.route("/message", methods=["POST"])
def handle_message():
    user_message = request.form["message"]

    # Add user's message to the chat history
    chat_history.append({"sender": "You", "content": user_message})

    # Generate response from Gemini
    try:
        # Add a small delay to show the loading indicator
        time.sleep(1)  # 500ms delay
        
        response = model.generate_content(user_message)
        print("Gemini Response:", response)  # Debug log
        bot_message = response.text
    except Exception as e:
        print(f"Gemini API Error (detailed):", str(e))  # More detailed error logging
        print(f"Error type:", type(e).__name__)  # Print the type of error
        bot_message = "Sorry, I'm having trouble processing your request."

    # Add bot's message to the chat history
    chat_history.append({"sender": "Bot", "content": bot_message})

    # Return the latest messages with a template that includes loading states
    return render_template("message.html", 
                         messages=chat_history[-2:])

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
