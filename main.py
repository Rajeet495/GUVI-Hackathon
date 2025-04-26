import streamlit as st
from modules.interview import start_interview
from modules.feedback import generate_feedback_pdf
from modules.analysis import display_analytics_dashboard
from modules.video import capture_video_input
from modules.resume import analyze_resume
from modules.utils import load_sentiment_model, initialize_text_to_speech
from modules.settings import display_sidebar_settings

# Initialize Sentiment Analysis and TTS
sentiment_pipeline = load_sentiment_model()
text_to_speech = initialize_text_to_speech()

# Initialize Session State
if "questions_answered" not in st.session_state:
    st.session_state.questions_answered = 0
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "analytics" not in st.session_state:
    st.session_state.analytics = {}

# Page Configuration
st.set_page_config(page_title="AI Interview Bot", layout="centered")
st.title("🤖 AI Interview Preparation Bot")

# Sidebar Settings
role, mode, persona, difficulty_level, num_questions, time_limit = display_sidebar_settings()

# Main App Functionality
if st.button("Start Interview"):
    start_interview(role, mode, persona, difficulty_level, num_questions, time_limit, sentiment_pipeline)

if st.sidebar.checkbox("View Performance Analytics"):
    display_analytics_dashboard()

resume_text = st.text_area("Paste your resume for AI feedback:")
if resume_text:
    analyze_resume(resume_text)

if st.sidebar.checkbox("Capture Video"):
    capture_video_input()

if st.sidebar.button("Download Feedback Report"):
    generate_feedback_pdf()