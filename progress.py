import streamlit as st
from datetime import datetime

class ProgressMonitor:
    def __init__(self):
        # Ensure 'transactions' is initialized
        if 'transactions' not in st.session_state:
            st.session_state.transactions = []

        if 'goal_amount' not in st.session_state:
            st.session_state.goal_amount = 0.0
        if 'goal_start' not in st.session_state:
            st.session_state.goal_start = datetime.today()
        if 'goal_end' not in st.session_state:
            st.session_state.goal_end = datetime.today()

    def set_goal_period(self, start_date, end_date):
        """Sets the period for the savings goal."""
        st.session_state.goal_start = start_date
        st.session_state.goal_end = end_date

    def calculate_progress(self):
        """Calculates the savings progress and the time progress."""
        # Calculate the total savings (sum of all positive amounts)
        total_savings = sum(amount for _, amount, _ in st.session_state.transactions if amount > 0)

        # Calculate the progress percentage towards the goal
        progress_percentage = (total_savings / st.session_state.goal_amount) * 100 if st.session_state.goal_amount > 0 else 0

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

# 貯金目標の期間を設定
st.header("貯金目標期間の設定")
start_date = st.date_input("開始日", value=st.session_state.goal_start)
end_date = st.date_input("終了日", value=st.session_state.goal_end)
progress_monitor.set_goal_period(start_date, end_date)

# 貯金目標の進捗を表示
progress_monitor.display_progress()
