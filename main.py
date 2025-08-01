
import streamlit as st
import pandas as pd
import requests

# Функция для загрузки списка компаний из YC Directory
def fetch_yc_companies(batch="S25"):
    url = "https://api.ycombinator.com/graphql"
    query = '''
    query ($batch: String!, $first: Int!, $after: String) {
      allCompanies(filter: {batches: [$batch]}, first: $first, after: $after) {
        edges {
          node {
            name
            website
            shortDescription
            ycUrl
          }
          cursor
        }
      }
    }
    '''
    variables = {"batch": batch, "first": 50, "after": None}
    results = []
    while True:
        resp = requests.post(url, json={"query": query, "variables": variables})
        data = resp.json()
        edges = data['data']['allCompanies']['edges']
        if not edges:
            break
        for edge in edges:
            node = edge['node']
            results.append({
                "name": node['name'],
                "website": node['website'],
                "description": node['shortDescription'],
                "yc_url": node['ycUrl']
            })
        variables['after'] = edges[-1]['cursor']
    return pd.DataFrame(results)

st.title("Y Combinator S25 Companies Tracker")
st.write("Список стартапов Y Combinator Summer 2025 (S25)")

if "data" not in st.session_state:
    with st.spinner("Загрузка данных с Y Combinator..."):
        st.session_state["data"] = fetch_yc_companies()

df = st.session_state["data"]

# Фильтр по поиску
search = st.text_input("Поиск по названию или описанию:")
if search:
    df = df[df.apply(lambda row: search.lower() in str(row["name"]).lower() or search.lower() in str(row["description"]).lower(), axis=1)]

st.dataframe(df)

# Кнопка скачать
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Скачать CSV", csv, "yc_s25_companies.csv", "text/csv")
