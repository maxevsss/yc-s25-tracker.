
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("yc_s25_data.csv")

st.title("Y Combinator Summer 2025 Companies Tracker")
st.write("Полный список стартапов YC Summer 2025 (112 компаний)")

df = load_data()

search = st.text_input("Поиск по названию или описанию:")
if search:
    df = df[df.apply(lambda row: search.lower() in str(row["name"]).lower() or search.lower() in str(row["description"]).lower(), axis=1)]

st.dataframe(df)

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Скачать CSV", csv, "yc_s25_companies.csv", "text/csv")
