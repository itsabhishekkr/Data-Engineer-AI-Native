import streamlit as st
import pandas as pd
import json

st.title("News Events AI Data Quality Dashboard")

df = pd.read_csv("data/processed/cleaned_news_events.csv")

st.subheader("Cleaned Records")
st.write(df.head())

st.metric("Total Records", len(df))

try:
    with open("data/processed/human_review_queue.json", "r") as f:
        review = json.load(f)

    st.metric("Human Review Queue", len(review))
    st.subheader("Review Queue")
    st.json(review[:10])

except FileNotFoundError:
    st.warning("No review queue found.")