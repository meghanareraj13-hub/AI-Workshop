"""
Configuration module for CampusAI.
Handles loading environment variables, Streamlit secrets, system prompts,
and application constants.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

# Load local .env file if available
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    load_dotenv()


def get_gemini_api_key() -> str | None:
    """
    Retrieve Gemini API key with fallback order:
    1. Streamlit secrets (if running inside Streamlit with secrets configured)
    2. Environment variable GEMINI_API_KEY
    """
    api_key = None

    # Check Streamlit secrets if streamlit is imported and secrets exist
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    # Fallback to os.environ
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        api_key = api_key.strip()
        if not api_key or api_key == "your_gemini_api_key_here":
            return None

    return api_key


# Model Configuration
DEFAULT_MODEL_NAME = "gemini-2.5-flash"

# System Prompt for CampusAI
SYSTEM_INSTRUCTION = """
You are CampusAI, a friendly, knowledgeable, and supportive AI College Assistant dedicated to helping college students succeed.

Your goals:
1. Provide simple, clear, and easy-to-understand explanations.
2. Use relevant real-world examples whenever appropriate.
3. Provide practical, step-by-step guidance for academic and career questions.
4. Assist students with college life, courses and subjects, study techniques, exam preparation, assignment guidance, internship searches, campus placement preparation, resume building, technical and HR interview guidance, and career planning.
5. Avoid overly dense, academic jargon unless explaining it clearly for beginners.
6. Admit when information is unavailable, uncertain, or subjective.
7. CRITICAL RULE: NEVER invent college-specific information such as specific semester exam dates, exact fee structures, institutional placement statistics, or faculty names/contact details. When asked about specific institution data, clearly and politely inform the student that you don't have access to specific college databases and advise them to check their official college portal, notice board, or consult their college administration.

Maintain an encouraging, empathetic, and professional tone at all times.
""".strip()

# Suggested Starter Questions
SUGGESTED_QUESTIONS = [
    "How can I prepare for campus placements?",
    "Explain the difference between internships and full-time jobs.",
    "What are the important topics in Python?",
    "How should I prepare for technical interviews?",
    "How can I create an effective resume?",
    "What are the best career options after graduation?",
]

# Application metadata
APP_TITLE = "CampusAI"
APP_SUBTITLE = "Smart College Assistant Chatbot"
WELCOME_MESSAGE = "Hello! I'm CampusAI, your smart college assistant. How can I help you today?"
