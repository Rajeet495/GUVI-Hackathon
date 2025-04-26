import streamlit as st
import pandas as pd

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "questions_answered" not in st.session_state:
    st.session_state.questions_answered = 0
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# Helper Functions
def display_interview_question():
    """Generates and displays a new interview question."""
    question = generate_question(f"Ask a {mode.lower()} interview question for a {role}")
    st.session_state.chat_history.append(("AI", question))
    st.subheader("🧠 Interview Question")
    st.markdown(question)

def analyze_sentiment(user_input):
    """Performs sentiment analysis on the user's input."""
    if user_input:
        sentiment_label, sentiment_score = get_sentiment_analysis(user_input)
        st.write(f"Sentiment: {sentiment_label} with confidence {sentiment_score:.2f}")
        return sentiment_score
    return 0

def record_audio():
    """Handles audio recording functionality."""
    audio_bytes = st_audiorec()
    if audio_bytes is not None:
        st.audio(audio_bytes, format="audio/wav")
        return audio_bytes
    return None

def handle_feedback_submission(user_input, sentiment_score):
    """Handles the process of submitting an answer and updating the state."""
    feedback = get_interactive_feedback(user_input)
    st.session_state.chat_history.append(("User", user_input))
    st.session_state.chat_history.append(("AI Feedback", feedback))
    st.session_state.total_score += sentiment_score
    st.session_state.questions_answered += 1
    st.success("Answer Submitted Successfully!")

def download_pdf_report():
    """Exports and provides a download link for the performance report."""
    pdf_path = export_feedback_as_pdf(st.session_state.chat_history)
    with open(pdf_path, "rb") as f:
        st.download_button("📄 Download Summary PDF", f, file_name="interview_summary.pdf")

def display_leaderboard():
    """Displays the leaderboard if data exists."""
    if st.session_state.leaderboard:
        leaderboard_df = pd.DataFrame(st.session_state.leaderboard, columns=["Name", "Score", "Badge"])
        st.dataframe(leaderboard_df)
        if st.button("Export Leaderboard to CSV"):
            csv_data = leaderboard_df.to_csv(index=False)
            st.download_button("Download CSV", csv_data, "leaderboard.csv", "text/csv")
    else:
        st.info("No leaderboard data yet.")

# Main Tabs
tabs = st.tabs([
    "🎤 Interview", "📄 Resume Review", "👥 Group Simulation", "📊 Performance & Report", "🏆 Leaderboard", "⚙️ Settings"
])

# ---------------------- TAB 1: INTERVIEW ----------------------
with tabs[0]:
    st.header("🎤 Interview Session")
    if st.button("Start Interview"):
        display_interview_question()

    if len(st.session_state.chat_history) > 0:
        st.subheader("🧠 Interview Question")
        st.markdown(st.session_state.chat_history[-1][1])

        user_input = st.text_area("Your Answer", key="interview_answer")
        sentiment_score = 0

        with st.expander("📈 Analyze Sentiment"):
            sentiment_score = analyze_sentiment(user_input)

        with st.expander("🎥 Video Capture"):
            if st.checkbox("Enable Webcam"):
                capture_video_input()

        with st.expander("🎧 Audio Recording"):
            record_audio()

        if st.button("Submit Answer"):
            handle_feedback_submission(user_input, sentiment_score)

# ---------------------- TAB 2: RESUME REVIEW ----------------------
with tabs[1]:
    st.header("📄 Resume Review")
    resume_text = st.text_area("Paste your resume text below:")
    if resume_text:
        resume_feedback = get_resume_feedback(resume_text)
        st.success(resume_feedback)

# ---------------------- TAB 3: GROUP SIMULATION ----------------------
with tabs[2]:
    st.header("👥 Group Interview Simulation")
    if simulate_group:
        group_feedback = group_interview_simulation()
        st.success(group_feedback)
    else:
        st.info("Enable 'Simulate Group Interview' from the sidebar to activate this.")

# ---------------------- TAB 4: PERFORMANCE & REPORT ----------------------
with tabs[3]:
    st.header("📊 Performance Report")
    if st.session_state.questions_answered > 0:
        avg_score = st.session_state.total_score / st.session_state.questions_answered
        st.metric(label="Average Score", value=f"{avg_score:.2f}")
    else:
        st.info("No answers submitted yet.")

    if st.button("Download PDF Report"):
        download_pdf_report()

# ---------------------- TAB 5: LEADERBOARD ----------------------
with tabs[4]:
    st.header("🏆 Leaderboard")
    display_leaderboard()

# ---------------------- TAB 6: SETTINGS ----------------------
with tabs[5]:
    st.header("⚙️ Extra Settings")
    if st.button("Activate Text-to-Speech"):
        text_to_speech.say("This is your interview session.")
        text_to_speech.runAndWait()

    feedback = st.text_area("Leave feedback for the app (optional)")
    if st.button("Submit Feedback") and feedback:
        st.session_state.chat_history.append({"user_feedback": feedback})
        st.success("Feedback submitted successfully!")