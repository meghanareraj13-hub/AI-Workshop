# CampusAI – Smart College Assistant Chatbot

CampusAI is a beginner-friendly, modern AI-powered College Assistant Chatbot designed to help undergraduate and graduate students navigate academic life, career preparation, and campus opportunities. Built using Python, Streamlit, and the official Google Gemini API (`google-genai` SDK).

---

## 📖 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Obtaining a Google Gemini API Key](#obtaining-a-google-gemini-api-key)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Screenshots](#screenshots)
- [Running Tests](#running-tests)
- [Security & Best Practices](#security--best-practices)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## 🎯 Overview

College students often face challenges finding trustworthy, instant guidance regarding subject selection, exam preparation, technical interview strategies, internship searches, resume building, and campus placements.

**CampusAI** acts as a 24/7 intelligent companion that:
- Delivers simple, step-by-step explanations with relatable examples.
- Provides actionable roadmaps for campus placements and internships.
- Transparently admits when institution-specific information (such as exact exam dates, fee breakdowns, or faculty contacts) requires checking official college administration portals rather than guessing.

---

## ✨ Key Features

1. **AI-Powered College Guidance:**
   - Real-time responses using Google Gemini API (`gemini-2.5-flash`).
   - Grounded system instructions preventing hallucination of college-specific administrative details.
2. **Interactive Streamlit UI:**
   - Clean, modern layout with customizable sidebar, custom avatars, and message bubbles.
   - Clickable suggested starter questions for rapid interaction.
   - Dynamic loading spinner while generating responses.
3. **Session State Chat Management:**
   - Multi-turn conversation history maintained seamlessly throughout the session.
   - **➕ New Chat** to restart your session with a clean slate.
   - **🗑️ Clear History** to erase stored conversation history anytime.
4. **Resilient Error Handling & Input Validation:**
   - Graceful warnings when `GEMINI_API_KEY` is missing or invalid.
   - Input validation guarding against empty messages.
   - Clear feedback for API rate limits and network issues.

---

## 🛠️ Technologies Used

- **Language:** Python 3.10+ (tested on Python 3.12)
- **Frontend / Framework:** [Streamlit](https://streamlit.io/)
- **Generative AI SDK:** Official Google GenAI SDK ([`google-genai`](https://github.com/googleapis/python-genai))
- **Environment Management:** [python-dotenv](https://github.com/theskumar/python-dotenv)
- **Testing:** [pytest](https://docs.pytest.org/)
- **Image / Assets:** [Pillow (PIL)](https://python-pillow.org/)

---

## 📁 Project Structure

```text
campusai/
├── app.py                  # Main Streamlit web application
├── gemini_service.py       # Google Gemini API integration service
├── config.py               # Application configuration, system prompts & constants
├── requirements.txt        # Python dependency manifest
├── .env.example            # Example environment variable template
├── .gitignore              # Git ignore configuration
├── README.md               # Detailed project documentation
└── assets/
    └── logo.png            # CampusAI logo graphic
```

---

## 🔑 Obtaining a Google Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Sign in with your Google account.
3. Click **"Create API Key"** and choose an existing Google Cloud project or create a new one.
4. Copy your newly generated API key.

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository_url>
cd <repository_folder>
```

### 2. Create and Activate a Virtual Environment
```bash
# On Linux / macOS
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to create your own `.env` file:
```bash
cp .env.example .env
```
Open `.env` in your text editor and insert your Gemini API key:
```env
GEMINI_API_KEY=AIzaSyYourActualKeyHere
```

*Note: In Streamlit Cloud deployments, you can alternatively set `GEMINI_API_KEY` directly in **App Settings -> Secrets**.*

---

## 💻 Running the Application

Launch the Streamlit app with:
```bash
streamlit run campusai/app.py
```
Or from the project root:
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 🖼️ Screenshots

### Chat Interface & Suggested Questions
```text
+-----------------------------------------------------------------------------------+
|  🎓 CampusAI   |  🎓 CampusAI - Smart College Assistant Chatbot                    |
|  AI College    |                                                                  |
|  Assistant     |  [✨ Need inspiration? Click a suggested question]               |
|                |  [👉 Campus Placements]      [👉 Internships vs Full-Time]       |
|  [+ New Chat]  |  [👉 Python Key Topics]      [👉 Technical Interviews]          |
|  [🗑️ Clear]    |                                                                  |
|                |  🎓 CampusAI: Hello! I'm CampusAI, your smart college assistant! |
|  💡 Features   |  🧑‍🎓 You: How should I prepare for technical interviews?         |
|  - Courses     |  🎓 CampusAI: Here is a structured 4-step preparation guide:     |
|  - Placements  |     1. Master Data Structures & Algorithms...                     |
|  - Interviews  |     2. Practice Mock Interviews...                                |
|                |  [ Ask any question about courses, exams, placements...     ^ ]  |
+-----------------------------------------------------------------------------------+
```

---

## 🧪 Running Tests

CampusAI includes unit and integration tests covering configuration, API key fallback, message formatting, and Gemini client operations.

Run tests using `pytest`:
```bash
python3 -m pytest -v
```

---

## 🔒 Security & Best Practices

- **Never Commit Secrets:** `.env` and `.streamlit/secrets.toml` are explicitly listed in `.gitignore`.
- **Environment Fallback:** API keys are read from environment variables or Streamlit secrets and never exposed to the frontend browser bundle.
- **Input Sanitization:** User messages are stripped and validated prior to transmission to the Gemini API.

---

## 🔮 Future Enhancements

- 📄 **Resume PDF Analyzer:** Upload a resume in PDF format and receive real-time ATS recommendations.
- 🗣️ **Voice Interaction:** Integrate Speech-to-Text and Text-to-Speech for conversational audio support.
- 🏛️ **College Portal Integration:** Allow institutions to hook CampusAI up to their official academic portal via RAG (Retrieval-Augmented Generation).
- 📅 **Mock Interview Simulator:** Interactive behavioral and technical interview practice scenarios.

---

## 📄 License

This project is licensed under the MIT License - feel free to adapt and expand for your college or workshop projects.
