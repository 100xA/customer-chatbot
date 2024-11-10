from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import markdown
import os
import time

app = Flask(__name__)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Store chat history
chat_history = []

@app.route("/")
def index():
    # Clear any existing chat history and add welcome message
    chat_history.clear()
    welcome_message = {
        "sender": "Bot",
        "content": "Hello! I'm your AI assistant. How can I help you today?"
    }
    chat_history.append(welcome_message)
    return render_template("index.html", messages=chat_history)

@app.route("/message", methods=["POST"])
def handle_message():
    user_message = request.form["message"]
    chat_history.append({"sender": "You", "content": user_message})

    # Add a small delay to show loading animation (500ms)
    time.sleep(1)

    # Define keywords for support-related queries
    support_keywords = [
        'hello', 'help', 'problem', 'issue', 'broken', 'not working', 'error',
        'how to', 'can\'t', 'doesn\'t work', 'support', 'trouble',
        'service', 'account', 'payment', 'order', 'refund'
    ]

    # Check if message contains any support-related keywords
    is_support_query = any(keyword in user_message.lower() for keyword in support_keywords)

    try:
        if not is_support_query:
            bot_message = "I apologize, but I'm specifically designed to help with customer support queries. Please ask me questions related to product issues, account help, or general support matters."
        else:
            response = model.generate_content(user_message)
            bot_message = response.text
            
        # Convert markdown to HTML
        bot_message = markdown.markdown(bot_message)
            
    except Exception as e:
        print(f"Gemini API Error (detailed):", str(e))
        print(f"Error type:", type(e).__name__)
        bot_message = "Sorry, I'm having trouble processing your request."

    chat_history.append({"sender": "Bot", "content": bot_message})
    return render_template("message.html", messages=chat_history[-2:])
