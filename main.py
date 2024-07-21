import streamlit as st
import api.polygon as pol
from chat.chat_agent import ChatAgent
import os

# Set the working directory
working_directory = os.environ.get("CURRENT_WORKING_DIRECTORY")  # Replace with your actual working directory path

# Streamlit app
st.title("Joseph's Data Analysis Assistant")

# Function to retrieve generated files
def get_generated_files():
    files = [f for f in os.listdir(working_directory) if f.endswith('.csv')]
    return files

# Streamlit sidebar form for data input
with st.sidebar:
    with st.form(key='my_form'):
        # Clear cached data and resources
        st.cache_data.clear()
        st.cache_resource.clear()

        # Input field for the symbol
        symbol = st.text_input(label="Symbol", key="symbol")

        # Input fields for last and next dates
        last_date = st.date_input(label="Last Date", key="last_date")
        next_date = st.date_input(label="Next Date", key="next_date")

        # Submit button
        submit_button = st.form_submit_button(label='Submit')

# Initialize a session state variable to keep track of the form submission status
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

# Process the form submission
if submit_button:
    # Validate input data
    if symbol and last_date and next_date:
        input_data = {
            "symbol": symbol,
            "last": str(last_date),
            "next": str(next_date),
        }

        # Call the API and get the response
        pol.agent_executor.invoke(input_data)

        # Mark the form as submitted
        st.session_state['submitted'] = True
    else:
        st.error("Please fill out all fields.")

# Display a list of generated files with options to delete or download
st.sidebar.header("Generated Files")
generated_files = get_generated_files()
for file in generated_files:
    st.sidebar.write(file)

# Chat window functionality
st.header("Chat with Joseph's Data Analysis Assistant")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Display chat history
for message in st.session_state['chat_history']:
    st.write(message)

# Input field for new message
new_message = st.text_input("Enter your message:")

# Button to send the message
if st.button("Send"):
    if new_message:
        # Append the new message to the chat history
        chat_agent_instance = ChatAgent.get_instance()
        st.session_state['chat_history'].append(f"You: {new_message}")
        
        try:
            response = chat_agent_instance.invoke(
                {"input": f"{new_message}"},
                config={"configurable": {"session_id": "polygon-api-query"}}
            )
        except RuntimeError as e:
            print(f"An error occurred: {e}")
     


        # Cleanup resources
        #chat_agent.cleanup()
        st.session_state['chat_history'].append(response)
        
        # Clear the input field after sending the message
        st.rerun()
    else:
        st.error("Please enter a message.")




