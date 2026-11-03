"""
CampusAI - Smart College Assistant Chatbot
Streamlit Application
"""

import os
from pathlib import Path
import streamlit as st

# Setup import path for modular imports
try:
    from config import (
        APP_TITLE,
        APP_SUBTITLE,
        WELCOME_MESSAGE,
        SUGGESTED_QUESTIONS,
        get_gemini_api_key,
    )
    from gemini_service import generate_response, GeminiServiceError
except ImportError:
    from campusai.config import (
        APP_TITLE,
        APP_SUBTITLE,
        WELCOME_MESSAGE,
        SUGGESTED_QUESTIONS,
        get_gemini_api_key,
    )
    from campusai.gemini_service import generate_response, GeminiServiceError

# Page setup
st.set_page_config(
    page_title=f"{APP_TITLE} - {APP_SUBTITLE}",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern styling
st.markdown(
    """
    <style>
    /* Main container styling */
    .main {
        background-color: #f8fafc;
    }
    .stChatMessage {
        border-radius: 12px;
        padding: 10px 14px;
        margin-bottom: 8px;
    }
    .header-container {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #e2e8f0;
    }
    .header-title {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3a8a;
    }
    .header-subtitle {
        margin: 0;
        color: #4b5563;
        font-size: 1.05rem;
    }
    .suggested-btn button {
        text-align: left;
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        background-color: #ffffff;
        color: #1e293b;
        font-size: 0.9rem;
        transition: all 0.2s ease-in-out;
        width: 100%;
        margin-bottom: 4px;
    }
    .suggested-btn button:hover {
        background-color: #eff6ff;
        border-color: #3b82f6;
        color: #1d4ed8;
    }
    .feature-badge {
        display: inline-block;
        padding: 4px 10px;
        background-color: #e0e7ff;
        color: #3730a3;
        border-radius: 9999px;
        font-size: 0.8rem;
        margin-right: 4px;
        margin-bottom: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Locate logo
LOGO_PATH = Path(__file__).resolve().parent / "assets" / "logo.png"
if not LOGO_PATH.exists():
    LOGO_PATH = Path(__file__).resolve().parent.parent / "assets" / "logo.png"

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


def reset_chat():
    """Resets chat history to fresh new session."""
    st.session_state.messages = []
    st.session_state.pending_prompt = None


def clear_history():
    """Clears all conversation history."""
    st.session_state.messages = []
    st.session_state.pending_prompt = None


# --- SIDEBAR ---
with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=90)
    st.title(f"🎓 {APP_TITLE}")
    st.caption("AI-Powered College & Career Assistant")

    st.markdown(
        """
        **CampusAI** helps undergraduate and graduate students navigate
        college academics, exams, projects, internships, and campus placements.
        """
    )

    st.markdown("---")
    st.subheader("⚙️ Session Controls")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ New Chat", use_container_width=True, help="Start a new conversation"):
            reset_chat()
            st.rerun()
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True, help="Clear all messages in history"):
            clear_history()
            st.rerun()

    st.markdown("---")
    st.subheader("💡 Key Features")
    st.markdown(
        """
        - 📚 **Courses & Subjects** guidance
        - 📝 **Exam & Assignment** strategies
        - 💼 **Internship & Placement** roadmap
        - 📄 **Resume & Interview** tips
        - 🧭 **Career Guidance** & skills advice
        """
    )

    st.markdown("---")
    st.subheader("ℹ️ About CampusAI")
    st.markdown(
        """
        Built with **Python**, **Streamlit**, and **Google Gemini API** (`google-genai` SDK).

        *Note: CampusAI provides general academic and career guidance. For specific college exam dates, fee receipts, or official notices, please check your university portal.*
        """
    )


# --- MAIN CONTENT ---
st.markdown(
    f"""
    <div class="header-container">
        <div>
            <h1 class="header-title">🎓 {APP_TITLE}</h1>
            <p class="header-subtitle">{APP_SUBTITLE} – Your 24/7 Academic & Career Companion</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Check API Key
api_key = get_gemini_api_key()

if not api_key:
    st.warning(
        "⚠️ **Google Gemini API Key is missing!**\n\n"
        "To get started:\n"
        "1. Obtain an API key at [Google AI Studio](https://aistudio.google.com/app/apikey).\n"
        "2. Add your key into `.env` file as `GEMINI_API_KEY=your_key` or in `.streamlit/secrets.toml`.\n"
        "3. Alternatively, you can test by temporarily setting `export GEMINI_API_KEY=\"...\"`.",
        icon="🔑",
    )

# Suggested Questions Section
with st.expander("✨ Need inspiration? Click a suggested question:", expanded=(len(st.session_state.messages) == 0)):
    st.markdown("<p style='font-size: 0.9rem; color: #4b5563;'>Select an example prompt below to ask CampusAI immediately:</p>", unsafe_allow_html=True)
    q_cols = st.columns(2)
    for idx, question in enumerate(SUGGESTED_QUESTIONS):
        target_col = q_cols[idx % 2]
        with target_col:
            if st.button(f"👉 {question}", key=f"sq_{idx}", use_container_width=True):
                st.session_state.pending_prompt = question
                st.rerun()

# Display Welcome Message
with st.chat_message("assistant", avatar="🎓"):
    st.write(WELCOME_MESSAGE)

# Display Conversation History
for msg in st.session_state.messages:
    role = msg.get("role")
    avatar = "🎓" if role == "assistant" else "🧑‍🎓"
    with st.chat_message(role, avatar=avatar):
        st.markdown(msg.get("content", ""))

# Determine Prompt to Process
prompt_to_process = None

# 1. From pending suggested question
if st.session_state.pending_prompt:
    prompt_to_process = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

# 2. From chat input
chat_input_val = st.chat_input("Ask any question about courses, exams, placements, or careers...")
if chat_input_val:
    prompt_to_process = chat_input_val

# Process Prompt
if prompt_to_process:
    clean_prompt = prompt_to_process.strip()
    if not clean_prompt:
        st.warning("Please type a valid question before sending.")
    elif not api_key:
        # Display user message first
        st.session_state.messages.append({"role": "user", "content": clean_prompt})
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(clean_prompt)
        # Display assistant warning
        warning_msg = (
            "I cannot answer your question right now because the **Gemini API Key** is not configured. "
            "Please configure `GEMINI_API_KEY` in your `.env` file or Streamlit secrets to enable AI responses."
        )
        st.session_state.messages.append({"role": "assistant", "content": warning_msg})
        with st.chat_message("assistant", avatar="🎓"):
            st.error(warning_msg)
    else:
        # Append and display user message
        st.session_state.messages.append({"role": "user", "content": clean_prompt})
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(clean_prompt)

        # Generate and display assistant response
        with st.chat_message("assistant", avatar="🎓"):
            with st.spinner("CampusAI is thinking..."):
                try:
                    # Pass previous chat messages as context (excluding the prompt just added)
                    history_context = st.session_state.messages[:-1]
                    ai_reply = generate_response(
                        api_key=api_key,
                        user_message=clean_prompt,
                        chat_history=history_context,
                    )
                    st.markdown(ai_reply)
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                except GeminiServiceError as err:
                    error_text = f"**Error:** {str(err)}"
                    st.error(error_text)
                    st.session_state.messages.append({"role": "assistant", "content": error_text})
                except Exception as err:
                    error_text = f"**Unexpected Error:** {str(err)}"
                    st.error(error_text)
                    st.session_state.messages.append({"role": "assistant", "content": error_text})
