import streamlit as st

# Streamlit app
st.title("Poly")

# Streamlit sidebar form
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

# Process the form submission
if submit_button:
    # Validate input data
    if symbol and last_date and next_date:
        input_data = {
            "symbol": symbol,
            "last": str(last_date),
            "next": str(next_date),
        }

        # Display the input data on the main screen
        st.write("Input Data:")
        st.json(input_data)

        # Call the examplegetjson function (assuming it's defined elsewhere)
        #examplegetjson(input_data)
    else:
        st.error("Please fill out all fields.")
