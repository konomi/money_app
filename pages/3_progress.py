import streamlit as st
from datetime import datetime

class ProgressMonitor:
    def __init__(self):
        # Ensure 'transactions' and goal-related session state variables are initialized
        if 'transactions' not in st.session_state:
            st.session_state.transactions = []
        if 'goal_amt' not in st.session_state:
            st.session_state.goal_amt = 0.0
        if 'goal_start' not in st.session_state:
            st.session_state.goal_start = datetime.today()
        if 'goal_end' not in st.session_state:
            st.session_state.goal_end = datetime.today()

    def calculate_progress(self):
        """Calculates the savings progress and the time progress."""
        # Calculate the total savings (sum of all positive amounts)
        total_savings = sum(amount for _, _, amount in st.session_state.transactions if amount > 0)

        # Calculate the progress percentage towards the goal
        progress_percentage = (total_savings / st.session_state.goal_amt) * 100 if st.session_state.goal_amt > 0 else 0

        # Calculate time progress based on the current date
        days_passed = (datetime.today().date() - st.session_state.goal_start).days
        total_days = (st.session_state.goal_end - st.session_state.goal_start).days
        time_progress = (days_passed / total_days) * 100 if total_days > 0 else 0

        return progress_percentage, time_progress

    def display_progress(self):
        """Displays the progress in the Streamlit app."""
        progress_percentage, time_progress = self.calculate_progress()

        st.write("貯金目標の進捗状況:")
        st.progress(progress_percentage / 100)  # Progress bar for savings goal
        st.write(f"進捗率: {progress_percentage:.2f}%")
        st.write(f"目標期間の進捗: {time_progress:.2f}% 経過")

# インスタンスを作成
progress_monitor = ProgressMonitor()

# 貯金目標の進捗を表示
progress_monitor.display_progress()
