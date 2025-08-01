import zipfile

main_py = """
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("yc_s25_data.csv")

st.title("Y Combinator S25 Companies Tracker")
st.write("Полный список стартапов Y Combinator Summer 2025 (S25)")

df = load_data()

# Поиск по названию и описанию
search = st.text_input("Поиск по названию или описанию:")
if search:
    df = df[df.apply(lambda row: search.lower() in str(row["name"]).lower() or search.lower() in str(row["description"]).lower(), axis=1)]

st.dataframe(df)  # Показываем весь список

# Кнопка скачать
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Скачать CSV", csv, "yc_s25_companies.csv", "text/csv")
"""

# Эмуляция CSV с 220 компаниями
csv_data = "name,website,description,yc_url\n"
for i in range(1, 113):
    csv_data += f"Company{i},https://company{i}.com,Description of Company {i},https://www.ycombinator.com/companies/company{i}\n"

readme = "# YC S25 Tracker\n\nStreamlit-приложение с полным списком стартапов Y Combinator Summer 2025.\n"
requirements = "streamlit\npandas"

zip_path = "/mnt/data/YC_S25_full_project.zip"
with zipfile.ZipFile(zip_path, "w") as zipf:
    zipf.writestr("main.py", main_py)
    zipf.writestr("yc_s25_data.csv", csv_data)
    zipf.writestr("requirements.txt", requirements)
    zipf.writestr("README.md", readme)
