import streamlit as st
import textwrap

# Streamlit app
st.title("Patricia's Pdf Assistant")

# Streamlit sidebar form
with st.sidebar:
    with st.form(key='my_form'):

        st.cache_data.clear()
        st.cache_resource.clear()
       
        request = st.text_area(
            label="Choose Symbol,Date,",
            max_chars=150,
            key="query",
            height=None
        )
        submit_button = st.form_submit_button(label='Submit')
# Process the form submission
if request and submit_button:
   
   