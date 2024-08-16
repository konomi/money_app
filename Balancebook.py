# balancebook.py
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

def calculate_totals(data):
    # 调试列名，显示数据中的列名
    st.write("Data Columns：", data.columns.tolist())

    # 将列名转换为小写并去除多余空格
    data.columns = data.columns.str.strip().str.lower()

    # 确保所需的列存在
    required_columns = ['date', 'genre', 'amount']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        st.error(f"missing: {', '.join(missing_columns)}")
        return {}, data

    # 确保时间列为 datetime 格式
    data['date'] = pd.to_datetime(data['date'])

    # 获取当前时间
    now = datetime.now()

    # 计算时间段
    one_week_ago = now - timedelta(weeks=1)
    one_month_ago = now - timedelta(days=30)
    six_months_ago = now - timedelta(days=182)  # 约为6个月
    one_year_ago = now - timedelta(days=365)

    # 定义各时间段
    time_periods = {
        'one week ': (one_week_ago, now),
        'one month ': (one_month_ago, now),
        'half year ': (six_months_ago, now),
        'one year ': (one_year_ago, now)
    }

    genre = ["Food", "Insurance", "Transport", "Utility Bills", "Shopping", "Entertainment", "Rent", "Wifi", "Phone Bills", "Other"]

    # 计算总收入和支出
    totals = {}
    for period_name, (start_date, end_date) in time_periods.items():
        period_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
        income_total = period_data[period_data['amount'] > 0]['amount'].sum()
        spending_total = abs(period_data[period_data['amount'] < 0]['amount'].sum())  # 支出为负数，因此取绝对值
        totals[f'{period_name}income'] = income_total
        totals[f'{period_name}spending'] = spending_total

    
    start_date1 = st.date_input("start date", value=data['date'].min().date())
    end_date1 = st.date_input("end date", value=data['date'].max().date())
    genre1 = st.selectbox("genre", genre)

    # 过滤数据
    if start_date1 or end_date1:
        data = data[data['date'] >= pd.to_datetime(start_date1)]
        data = data[data['date'] <= pd.to_datetime(end_date1)]
        total_income = data[data['amount'] > 0]['amount'].sum()
        total_spending = abs(data[data['amount'] <= 0]['amount'].sum())
        st.write(f"total income in the period: {total_income}")
        st.write(f"total spending in the period: {total_spending}")

    if genre1:
        data = data[data['genre'] == genre1]
        total_genre_spending = abs(data['amount'].sum())
        st.write(f"total spending of the genre: {total_genre_spending}")
    


    # 将计算结果保存到 df2.csv 文件中
    totals_df = pd.DataFrame([totals])
    totals_df.to_csv('df2.csv', index=False, mode='w', encoding='utf-8-sig')


    return totals, data

def main():
    st.title('Balance Book')

    # 上传 CSV 文件
    uploaded_file = st.file_uploader("Please upload the finance file", type=["csv"])

    if uploaded_file is not None:
        # 加载数据
        data = pd.read_csv(uploaded_file)

        # 显示原始数据
        st.subheader('Raw Data')
        st.dataframe(data)

        # 计算总和并更新数据
        totals, updated_data = calculate_totals(data)

        # 显示计算结果
        if totals:
            st.subheader('Result')
            for key, value in totals.items():
                st.write(f"{key}: {value}")

            # 保存更新后的数据到原始 CSV 文件
            #updated_data.to_csv(uploaded_file.name, index=False, encoding='utf-8-sig')
            #st.success(f"计算结果已保存回文件: {uploaded_file.name}")

            # 提供下载链接
            updated_csv = updated_data.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="Download the uploaded csv",
                data=updated_csv,
                file_name=uploaded_file.name,
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
