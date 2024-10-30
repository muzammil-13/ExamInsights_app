import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Assuming API_URL is correct from previous code
API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = "http://0.0.0.0:8000/v1/pw_ai_answer"

def get_response(prompt):
    """Gets a response from the ExamInsights API."""
    headers = {
        "accept": "*/*",
        "Content-Type": "application/json"
    }
    data = {"prompt": prompt}
    response = requests.post(API_URL, headers=headers, json=data) 
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

# --- Streamlit App ---
st.set_page_config(page_title="ExamInsights", page_icon=":books:")

st.title("ExamInsights :books:")
st.write("Get insights from past exam papers to ace your next test!")

with st.form("question_form"):
    prompt = st.text_area("Enter your question about the exam topic: (eg., DSA related questions)", height=100)
    submitted = st.form_submit_button("Get Insights")

    if submitted and prompt:
        with st.spinner("Analyzing past exams..."):
            try:
                response = get_response(prompt)
                st.markdown(f"**Answer:** {response}") 
            except requests.exceptions.RequestException as e:
                st.error(f"Error communicating with the API: {e}")
    elif submitted and not prompt:
        st.warning("Please enter a question.") 
