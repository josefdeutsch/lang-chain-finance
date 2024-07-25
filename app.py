from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
import os
import api.polygon as pol
from chat.chat_agent import ChatAgent, SingletonMeta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flash messages and session management

# Set the working directory
working_directory = os.environ.get("CURRENT_WORKING_DIRECTORY", '.')  # Replace with your actual working directory path

# Function to retrieve generated files
def get_generated_files():
    files = [f for f in os.listdir(working_directory) if f.endswith('.csv')]
    return files


@app.route('/reset', methods=['POST'])
def reset():
    SingletonMeta.reset_instance(ChatAgent)
    return jsonify({"message": "Agent reset successfully"})


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
            flash("Query submitted successfully.", "success")
        else:
            flash("Please fill out all fields.", "error")

    generated_files = get_generated_files()
    return render_template('index.html', generated_files=generated_files, last_message=session.pop('last_message', ''))

@app.route('/chat', methods=['POST'])
def chat():
    new_message = request.form.get('new_message')
    if new_message:
        chat_agent_instance = ChatAgent.get_instance()

        try:
            response = chat_agent_instance.invoke(
                {"input": new_message},
                config={"configurable": {"session_id": "polygon-api-query"}}
            )
        except RuntimeError as e:
            response = f"An error occurred: {e}"

        session['last_message'] = f"You: {new_message}<br>Bot: {response}"
    else:
        flash("Please enter a message.", "error")

    return redirect(url_for('index'))

@app.teardown_appcontext
def shutdown_session(exception=None):
    # Clean up resources
    chat_agent_instance = ChatAgent.get_instance()
    chat_agent_instance.cleanup()

if __name__ == '__main__':
    app.run(debug=True)
