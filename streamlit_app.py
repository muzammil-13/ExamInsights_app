import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch API_URL from environment variables, fallback to default local Docker url
API_URL = os.getenv("EXAMINSIGHTS_API_URL", "http://0.0.0.0:8000/v1/pw_ai_answer")
TIMEOUT = int(os.getenv("EXAMINSIGHTS_TIMEOUT_SECONDS", 45))

def get_response(prompt):
    """Gets a response from the ExamInsights API."""
    headers = {
        "accept": "*/*",
        "Content-Type": "application/json"
    }
    data = {"prompt": prompt}
    response = requests.post(API_URL, headers=headers, json=data, timeout=TIMEOUT) 
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
                raw_response = get_response(prompt)
                
                # Extract the actual answer text from the JSON response body
                answer_text = raw_response
                if isinstance(raw_response, dict):
                    if "response" in raw_response:
                        answer_text = raw_response["response"]
                    elif "answer" in raw_response:
                        answer_text = raw_response["answer"]
                    elif "text" in raw_response:
                        answer_text = raw_response["text"]
                    elif "choices" in raw_response and len(raw_response["choices"]) > 0:
                        answer_text = raw_response["choices"][0].get("message", {}).get("content", str(raw_response))
                    else:
                        # Fallback for unexpected dictionary structures
                        answer_text = str(raw_response)
                
                st.markdown(f"**Answer:**\n\n{answer_text}") 
            except requests.exceptions.RequestException as e:
                st.error(f"Error communicating with the API: {e}")
    elif submitted and not prompt:
        st.warning("Please enter a question.") 
