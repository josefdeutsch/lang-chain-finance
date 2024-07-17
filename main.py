import streamlit as st
import api.polygon as pol
import os

# Set the working directory
working_directory = os.getenv('CURRENT_WORKING_DIRECTORY')  # Replace with your actual working directory path


# Streamlit app
st.title("Poly")

# Function to retrieve generated files
def get_generated_files():
    files = [f for f in os.listdir(working_directory) if f.endswith('.csv')]
    return files

# Function to delete a file
def delete_file(file_name):
    file_path = os.path.join(working_directory, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        st.success(f"File {file_name} deleted successfully.")

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
        response = pol.agent_executor.invoke(input_data)
        st.write(response)

        # Mark the form as submitted
        st.session_state['submitted'] = True
    else:
        st.error("Please fill out all fields.")

# Function to retrieve the file content
def retrieve_file(symbol):
    file_path = os.path.join(working_directory, f"{symbol}.csv")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read()
    return None

# Second form for file generation
if st.session_state['submitted']:
    with st.form(key='file_form'):
        # Submit button for file generation
        generate_file_button = st.form_submit_button(label='Generate File')

    # Process the file form submission
    if generate_file_button:
        # Retrieve the file content
        file_content = retrieve_file(symbol)

        if file_content:
            st.success(f"File {symbol}.csv generated and available for download.")
            st.download_button(label="Download File", data=file_content, file_name=f"{symbol}.csv")
        else:
            st.error(f"File {symbol}.csv generation failed or file not found. Please try again.")

# Display a list of generated files with options to delete or download
st.sidebar.header("Generated Files")
generated_files = get_generated_files()
for file in generated_files:
    file_path = os.path.join(working_directory, file)
    with st.sidebar:
        st.write(file)
        with open(file_path, "r") as f:
            file_content = f.read()
        st.download_button(label=f"Download {file}", data=file_content, file_name=file)
        if st.button(f"Delete {file}"):
            delete_file(file)
            st.experimental_rerun()  # Refresh the page to update the list
