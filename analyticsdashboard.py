import streamlit as st
import pandas as pd

def display_analytics_dashboard():
    st.subheader("📊 Performance Analytics")
    performance_data = {
        "Questions Answered": [st.session_state.questions_answered],
        "Total Score": [st.session_state.total_score],
    }
    df = pd.DataFrame(performance_data)
    st.bar_chart(df)
    st.write(df)