from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import api.polygon as pol
from chat.chat_agent import ChatAgent
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for session management

# Set the working directory
working_directory = os.environ.get("CURRENT_WORKING_DIRECTORY", '.')  # Replace with your actual working directory path

# Function to retrieve generated files
def get_generated_files():
    files = [f for f in os.listdir(working_directory) if f.endswith('.csv')]
    return files

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        last_date = request.form.get('last_date')
        next_date = request.form.get('next_date')

        if symbol and last_date and next_date:
            input_data = {
                "symbol": symbol,
                "last": last_date,
                "next": next_date,
            }

            # Call the API and get the response
            pol.agent_executor.invoke(input_data)

            # Mark the form as submitted
            session['submitted'] = True
        else:
            flash("Please fill out all fields.", "error")

    generated_files = get_generated_files()
    return render_template('index.html', generated_files=generated_files)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == 'POST':
        new_message = request.form.get('new_message')
        if new_message:
            # Append the new message to the chat history
            chat_agent_instance = ChatAgent.get_instance()
            session['chat_history'].append(f"You: {new_message}")

            try:
                response = chat_agent_instance.invoke(
                    {"input": f"{new_message}"},
                    config={"configurable": {"session_id": "polygon-api-query"}}
                )
            except RuntimeError as e:
                response = f"An error occurred: {e}"

            session['chat_history'].append(response)
            return redirect(url_for('chat'))
        else:
            flash("Please enter a message.", "error")

    return render_template('chat.html', chat_history=session['chat_history'])

if __name__ == '__main__':
    app.run(debug=True)
