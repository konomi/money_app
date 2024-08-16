import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# Input field")
st.sidebar.header("Input field")
st.write(
    """Input field"""
)

class input_field:
    def __init__(self):
        # st.session_state を使って支出や収入を保持する
        if 'transactions' not in st.session_state:
            st.session_state.transactions = []
        if 'goal_amt' not in st.session_state:
            st.session_state.goal_amt = 0.0
        if 'goal_start' not in st.session_state:
            st.session_state.goal_start = datetime.today()
        if 'goal_end' not in st.session_state:
            st.session_state.goal_end = datetime.today()
        if 'spending_input' not in st.session_state:
            st.session_state.spending_input = 0.0
        if 'income_date' not in st.session_state:
            st.session_state.income_date = datetime.today()
        if 'income_amount' not in st.session_state:
            st.session_state.income_amount = 0.0

    def get_goal(self):
        """貯金目標額と期間を設定する関数"""
        st.header("貯金目標の設定")
        goal_amt = st.number_input("貯金目標額を入力してください:", min_value=0.0, format="%f", key="goal_amt_input")
        goal_start = st.date_input("目標開始日を入力してください:", value=st.session_state.goal_start, key="goal_start_input")
        goal_end = st.date_input("目標終了日を入力してください:", value=st.session_state.goal_end, key="goal_end_input")
        
        if st.button("目標を設定"):
            st.session_state.goal_amt = goal_amt
            st.session_state.goal_start = goal_start
            st.session_state.goal_end = goal_end
            self.save_goal_to_csv()  # 目標設定後にCSVに自動保存
            st.success(f"貯金目標が設定されました。")
            st.write(f"貯金目標額: ¥{st.session_state.goal_amt}")
            st.write(f"目標期間: {st.session_state.goal_start} から {st.session_state.goal_end}")

    def get_income(self):
        """収入を追加する関数"""
        st.header("収入の入力")
        income_date = st.date_input("収入日を入力してください:", value=st.session_state.income_date, key="income_date_input")
        income = st.number_input("収入を入力してください:", min_value=0.0, format="%f", key="income_amount_input")
        
        if st.button("収入を追加"):
            st.session_state.transactions.append((income_date, "Income", income))
            self.save_transactions_to_csv()  # 収入が追加されたらCSVに自動保存
            st.success(f"¥{income} の収入が追加されました。")

    def add_spending(self):
        """支出を追加する関数"""
        st.header("支出の入力")
        date = st.date_input("日付を入力してください:", value=datetime.today())
        genre = st.selectbox("ジャンルを選択してください:", ["Food", "Insurance", "Transport", "Utility Bills", "Shopping", "Entertainment", "Rent", "Wifi", "Phone Bills", "Other"])
        expense = st.number_input("使ったお金を入力してください:", min_value=0.0, format="%f", key="spending_input")
        
        if st.button("支出を追加"):
            st.session_state.transactions.append((date, genre, -expense))
            self.save_transactions_to_csv()  # 支出が追加されたらCSVに自動保存
            st.success(f"¥{expense} の支出が追加されました。")
            st.session_state.spending_input = 0.0

    def save_goal_to_csv(self):
        """貯金目標額のデータをCSVファイルに保存する関数"""
        goal_data = {
            "goal_start": [st.session_state.goal_start],
            "goal_end": [st.session_state.goal_end],
            "goal_amt": [st.session_state.goal_amt]
        }
        df = pd.DataFrame(goal_data)
        df.to_csv("goal_data.csv", index=False)
        st.success("貯金目標データがCSVファイルに保存されました。")

    def save_transactions_to_csv(self):
        """取引データをCSVファイルに保存する関数"""
        df = pd.DataFrame(st.session_state.transactions, columns=["date", "genre", "amount"])
        df.to_csv("transactions.csv", index=False)
        st.success("取引データがCSVファイルに保存されました。")

# インスタンスを作成
infi = input_field()

st.title("MoneyApp")

# 貯金目標の設定
infi.get_goal()

# 収入の追加
infi.get_income()

# 支出の追加
infi.add_spending()

# 入力された内容を表示
st.write("詳細な取引履歴:")
st.write(st.session_state.transactions)
