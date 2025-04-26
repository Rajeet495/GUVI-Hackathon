import streamlit as st
from modules.utils import get_sentiment_analysis, generate_question, get_interactive_feedback

def start_interview(role, mode, persona, difficulty_level, num_questions, time_limit, sentiment_pipeline):
    st.session_state.chat_history.append(("AI", generate_question(role, mode, difficulty_level)))
    
    if len(st.session_state.chat_history) > 0:
        st.subheader("🧠 Interview Question")
        st.markdown(st.session_state.chat_history[-1][1])

        user_input = st.text_area("Your Answer", key="answer_input")
        if user_input:
            sentiment_label, sentiment_score = get_sentiment_analysis(user_input, sentiment_pipeline)
            st.write(f"Sentiment: {sentiment_label} with confidence {sentiment_score:.2f}")
            
            feedback = get_interactive_feedback(user_input)
            st.session_state.chat_history.append(("User", user_input))
            st.session_state.chat_history.append(("AI Feedback", feedback))
            st.session_state.total_score += sentiment_score
            st.session_state.questions_answered += 1

            # Show Performance Analysis
            st.subheader("📊 Performance Analysis")
            avg_score = st.session_state.total_score / st.session_state.questions_answered
            st.write(f"Average Score: {avg_score:.2f}")