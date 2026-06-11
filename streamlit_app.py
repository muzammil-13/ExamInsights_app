import os
import logging
from datetime import datetime
from typing import Any, Dict, Union

import requests
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

@st.cache_resource
def setup_logger():
    """Configures the logger exactly once per Streamlit server runtime."""
    LOG_DIR = os.getenv("LOG_DIR", "/logs")
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
    except OSError:
        LOG_DIR = "logs"
        os.makedirs(LOG_DIR, exist_ok=True)

    log_filename = os.path.join(LOG_DIR, f"streamlit_app_{datetime.now().strftime('%Y%m%d')}.log")
    logger = logging.getLogger("streamlit_app")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        console_handler.setFormatter(console_formatter)

        file_handler = logging.FileHandler(log_filename)
        file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(file_formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.info(f"Streamlit UI initialized. Log file: {log_filename}")
    return logger

logger = setup_logger()

API_URL = os.getenv("EXAMINSIGHTS_API_URL", "http://localhost:8000/v1/pw_ai_answer")
TIMEOUT = int(os.getenv("EXAMINSIGHTS_TIMEOUT_SECONDS", "45"))

ROLE_GUIDANCE = {
    "Student": {
        "description": "Study guidance and revision planning",
        "instruction": (
            "You are helping a student prepare for exams. Focus on clear explanations, "
            "high-yield topics, repeated question patterns, weak areas, and practical "
            "revision steps."
        ),
        "presets": {
            "Custom question (type below)": "",
            "Likely exam topics": (
                "Identify the most likely exam topics from the uploaded papers. "
                "Explain why each topic matters and suggest a revision order."
            ),
            "Weak-area revision plan": (
                "Create a focused revision plan for topics that appear difficult or "
                "frequently tested. Include short practice prompts."
            ),
            "Explain previous questions": (
                "Explain recurring question patterns in simple language and show how "
                "I should prepare answers."
            ),
        },
    },
    "Educator": {
        "description": "Curriculum coverage and question-pattern analysis",
        "instruction": (
            "You are helping an educator analyze exam papers. Focus on topic coverage, "
            "frequency, curriculum alignment, assessment patterns, and actionable "
            "teaching insights."
        ),
        "presets": {
            "Custom question (type below)": "",
            "Topic frequency analysis": (
                "Analyze which topics appear most often across the uploaded papers "
                "and group them by frequency."
            ),
            "Curriculum coverage gaps": (
                "Identify curriculum areas that seem under-tested or over-tested in "
                "the available papers."
            ),
            "Question-pattern summary": (
                "Summarize repeated question formats, difficulty signals, and "
                "assessment trends for educators."
            ),
        },
    },
}


def compose_prompt(role, preset, custom_prompt):
    role_config = ROLE_GUIDANCE[role]
    preset_prompt = role_config["presets"][preset]
    user_prompt = custom_prompt.strip() or preset_prompt

    if not user_prompt:
        return None

    return f"""
{role_config["instruction"]}

Use the indexed exam-paper content and any available document metadata such as filename, source path, and modified time when it helps the answer.

Selected analysis preset:
{preset_prompt}

User question:
{user_prompt}
""".strip()


def extract_answer(raw_response):
    if not isinstance(raw_response, dict):
        return raw_response

    for key in ("response", "answer", "result", "text"):
        if key in raw_response:
            return raw_response[key]

    choices = raw_response.get("choices", [])
    if choices:
        message = choices[0].get("message", {})
        return message.get("content", str(raw_response))

    return str(raw_response)


def get_response(prompt: str) -> Dict[str, Any]:
    """Sends the formatted prompt to the Pathway backend and returns the JSON response."""
    logger.info(f"Sending prompt to backend: {prompt[:50]}...")
    headers = {
        "accept": "*/*",
        "Content-Type": "application/json",
    }
    response = requests.post(
        API_URL,
        headers=headers,
        json={"prompt": prompt},
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    logger.info("Successfully received response from backend")
    return response.json()


def check_backend() -> bool:
    """Checks if the Pathway backend is reachable."""
    logger.debug("Checking backend reachability...")
    try:
        response = requests.get(API_URL, timeout=5)
        return response.status_code < 500 or response.status_code in {404, 405}
    except requests.exceptions.RequestException:
        logger.warning("Backend is unreachable.")
        return False


def record_status(is_online: bool) -> None:
    """Updates the session state with the latest backend availability status."""
    st.session_state.backend_online = is_online
    st.session_state.last_synced = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


st.set_page_config(page_title="ExamInsights", page_icon=":books:", layout="wide")

if "backend_online" not in st.session_state:
    st.session_state.backend_online = None
if "last_synced" not in st.session_state:
    st.session_state.last_synced = None

st.title("ExamInsights :books:")
st.caption("Live RAG insights from the PDFs in the data folder.")

status_col, sync_col = st.columns([3, 1])
with status_col:
    if st.session_state.backend_online is True:
        st.success("Backend reachable")
    elif st.session_state.backend_online is False:
        st.error("Backend unavailable")
    else:
        st.info("Backend status not checked yet")

    if st.session_state.last_synced:
        st.caption(f"Last synced: {st.session_state.last_synced}")
    else:
        st.caption("Last synced: never")

with sync_col:
    if st.button("Sync now", use_container_width=True):
        record_status(check_backend())
        st.rerun()

role = st.radio("Choose your role", list(ROLE_GUIDANCE.keys()), horizontal=True)
role_config = ROLE_GUIDANCE[role]
st.caption(role_config["description"])

preset = st.selectbox("Analysis preset", list(role_config["presets"].keys()))

with st.form("question_form"):
    custom_prompt = st.text_area(
        "Ask about the uploaded exam papers",
        placeholder="Example: Which DSA topics are repeated most often?",
        height=120,
    )
    submitted = st.form_submit_button("Get insights", use_container_width=True)

    if submitted:
        prompt = compose_prompt(role, preset, custom_prompt)
        if not prompt:
            st.warning("Please select an analysis preset or type a custom question.")
        else:
            with st.spinner("Analyzing past exams..."):
                try:
                    raw_response = get_response(prompt)
                    record_status(True)
                    st.markdown("### Answer")
                    st.markdown(str(extract_answer(raw_response)))
                except requests.exceptions.Timeout:
                    logger.error("Backend request timed out.")
                    record_status(False)
                    st.error(
                        "The backend took too long to respond. Try again after the "
                        "index finishes syncing."
                    )
                except requests.exceptions.RequestException as exc:
                    logger.error(f"Error communicating with the API: {exc}")
                    record_status(False)
                    st.error(f"Error communicating with the API: {exc}")
